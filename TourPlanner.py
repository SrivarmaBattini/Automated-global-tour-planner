import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import numpy as np
from tkcalendar import DateEntry
from typing import List, Dict, Tuple, Set
import json
import folium
import webbrowser
import os

# --- Load Data ---
def load_country_data(filepath: str) -> Dict:
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Data file not found at {filepath}")
        return {}
    except json.JSONDecodeError:
        messagebox.showerror("Error", f"Could not decode JSON from {filepath}")
        return {}

country_data = load_country_data('data.json')

# --- Data Handling Class ---
class CountryData:
    def __init__(self, country_data_dict: Dict):
        self.countries_data = country_data_dict
        if not self.countries_data:
            self.all_interests = []
        else:
            self.all_interests = sorted(list(set(
                interest for country in self.countries_data.values()
                for interest in country.get('interests', [])
            )))

# --- Optimization Logic ---
class TourOptimizer:
    def __init__(self, country_data: CountryData):
        self.country_data = country_data

    def calculate_distance(self, coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
        return np.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

    def solve_tsp(self, selected_countries: List[str], home_country: str) -> List[str]:
        if not selected_countries:
            return [home_country, home_country]

        if home_country in selected_countries:
            selected_countries.remove(home_country)

        route = [home_country]
        unvisited = set(selected_countries)
        current = home_country

        while unvisited:
            next_country = min(
                unvisited,
                key=lambda x: self.calculate_distance(
                    tuple(self.country_data.countries_data[current]["coordinates"]),
                    tuple(self.country_data.countries_data[x]["coordinates"])
                )
            )
            route.append(next_country)
            unvisited.remove(next_country)
            current = next_country

        route.append(home_country)
        return route

    def calculate_country_interest_score(self, country: str, selected_interests: Set[str]) -> int:
        country_interests = set(self.country_data.countries_data[country].get("interests", []))
        return len(country_interests.intersection(selected_interests))

    def distribute_days(self, total_days: int, route: List[str],
                       selected_interests: Set[str]) -> Dict[str, int]:
        days_per_country = {}
        countries_to_visit = route[1:-1]
        if not countries_to_visit:
            return {}

        interest_scores = {
            country: self.calculate_country_interest_score(country, selected_interests)
            for country in countries_to_visit
        }

        total_score = sum(interest_scores.values())
        if total_score == 0:
            days_per = total_days // len(countries_to_visit)
            remainder = total_days % len(countries_to_visit)
            days_per_country = {country: days_per for country in countries_to_visit}
            for i in range(remainder):
                days_per_country[countries_to_visit[i]] += 1
        else:
            proportional_days = {
                country: (interest_scores[country] / total_score) * total_days
                for country in countries_to_visit
            }
            
            days_per_country = {c: int(d) for c, d in proportional_days.items()}
            remaining_days = total_days - sum(days_per_country.values())
            
            sorted_by_remainder = sorted(countries_to_visit, key=lambda c: proportional_days[c] - days_per_country[c], reverse=True)
            for i in range(remaining_days):
                days_per_country[sorted_by_remainder[i]] += 1

        return days_per_country

# --- GUI Class ---
class TourPlannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("✈️ Automated Global Tour Planner")
        self.country_data = CountryData(country_data)
        if not self.country_data.countries_data:
            self.root.destroy()
            return
            
        self.optimizer = TourOptimizer(self.country_data)
        # ... (GUI setup remains the same) ...
        style = ttk.Style()
        style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'))
        style.configure('Subheader.TLabel', font=('Helvetica', 12))
        style.configure('Custom.TButton', font=('Helvetica', 11, 'bold'))
        
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=3)
        main_frame.grid_columnconfigure(0, weight=1)

        self.input_frame = ttk.LabelFrame(main_frame, padding="15", text="Travel Parameters")
        self.input_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.output_frame = ttk.LabelFrame(main_frame, padding="15", text="Travel Itinerary")
        self.output_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.interest_vars = {}
        self.create_input_fields()
        self.create_output_display()

    def create_input_fields(self):
        # This method remains the same as the previous version
        header = ttk.Label(self.input_frame, text="Plan Your Journey", style='Header.TLabel')
        header.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        ttk.Label(self.input_frame, text="Number of Countries:", style='Subheader.TLabel').grid(row=1, column=0, pady=8, sticky='w')
        self.num_countries = ttk.Entry(self.input_frame)
        self.num_countries.grid(row=1, column=1, pady=8, sticky='ew')
        ttk.Label(self.input_frame, text="Travel Interests:", style='Subheader.TLabel').grid(row=2, column=0, columnspan=2, pady=(15, 5), sticky='w')
        interests_canvas = tk.Canvas(self.input_frame, borderwidth=0, height=200)
        interests_frame = ttk.Frame(interests_canvas)
        scrollbar = ttk.Scrollbar(self.input_frame, orient="vertical", command=interests_canvas.yview)
        interests_canvas.configure(yscrollcommand=scrollbar.set)
        interests_canvas.grid(row=3, column=0, columnspan=2, sticky='nsew', pady=5)
        scrollbar.grid(row=3, column=2, sticky='ns')
        interests_canvas.create_window((0, 0), window=interests_frame, anchor='nw')
        for i, interest in enumerate(self.country_data.all_interests):
            var = tk.BooleanVar()
            self.interest_vars[interest] = var
            cb = ttk.Checkbutton(interests_frame, text=interest.title(), variable=var)
            cb.grid(row=i // 2, column=i % 2, sticky='w', padx=10, pady=2)
        interests_frame.bind("<Configure>", lambda e: interests_canvas.configure(scrollregion=interests_canvas.bbox("all")))
        dates_frame = ttk.LabelFrame(self.input_frame, text="Travel Dates", padding=10)
        dates_frame.grid(row=4, column=0, columnspan=2, pady=15, sticky='ew')
        ttk.Label(dates_frame, text="Start:").grid(row=0, column=0, padx=5)
        self.start_date = DateEntry(dates_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='mm/dd/yy')
        self.start_date.grid(row=0, column=1, padx=5)
        ttk.Label(dates_frame, text="End:").grid(row=0, column=2, padx=5)
        self.end_date = DateEntry(dates_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='mm/dd/yy')
        self.end_date.grid(row=0, column=3, padx=5)
        ttk.Label(self.input_frame, text="Budget (USD):", style='Subheader.TLabel').grid(row=5, column=0, pady=8, sticky='w')
        self.budget = ttk.Entry(self.input_frame)
        self.budget.grid(row=5, column=1, pady=8, sticky='ew')
        ttk.Label(self.input_frame, text="Home Country:", style='Subheader.TLabel').grid(row=6, column=0, pady=8, sticky='w')
        self.starting_country = ttk.Combobox(self.input_frame, values=sorted(list(self.country_data.countries_data.keys())))
        self.starting_country.grid(row=6, column=1, pady=8, sticky='ew')
        generate_btn = ttk.Button(self.input_frame, text="Generate Itinerary & Map 🗺️", style='Custom.TButton', command=self.generate_itinerary)
        generate_btn.grid(row=7, column=0, columnspan=2, pady=20, sticky='ew')

    def create_output_display(self):
        # This method remains the same
        self.result_text = tk.Text(self.output_frame, wrap=tk.WORD, font=('Helvetica', 11), padx=10, pady=10, relief="sunken", borderwidth=1)
        scrollbar = ttk.Scrollbar(self.output_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.result_text.configure(yscrollcommand=scrollbar.set)
        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(0, weight=1)
        welcome_msg = "🌍 Welcome to the Automated Global Tour Planner!\n\n" \
                      "1. Select the number of countries, your interests, dates, and budget.\n" \
                      "2. Choose your home country.\n" \
                      "3. Click 'Generate Itinerary & Map' to get your personalized travel plan.\n\n" \
                      "Your itinerary will appear here, and a map of your route will open in your browser."
        self.result_text.insert("1.0", welcome_msg)

    def get_selected_interests(self) -> Set[str]:
        # This method remains the same
        return {interest for interest, var in self.interest_vars.items() if var.get()}

    def select_countries(self, interests: Set[str], num_countries: int, home_country: str) -> List[str]:
        # This method remains the same
        country_scores = {}
        for country, data in self.country_data.countries_data.items():
            if country != home_country:
                matching_interests = len(set(data.get("interests", [])) & interests)
                if matching_interests > 0:
                    country_scores[country] = matching_interests
        sorted_countries = sorted(country_scores.keys(), key=lambda c: country_scores[c], reverse=True)
        return sorted_countries[:num_countries]

    def calculate_total_cost(self, route: List[str], days_distribution: Dict[str, int]) -> float:
        total_cost = 0.0
        # Travel to each country
        for country in route[1:-1]:
            data = self.country_data.countries_data[country]
            days = days_distribution.get(country, 0)
            total_cost += data.get('avg_travel_cost', 0) + (data.get('avg_accommodation_cost', 0) * days)
        
        # Cost to return home from the last country
        if len(route) > 2:
             total_cost += self.country_data.countries_data[route[-2]].get('avg_travel_cost', 0)
        
        return total_cost

    def generate_itinerary(self):
        # *** THIS IS THE MODIFIED METHOD ***
        try:
            num_countries = int(self.num_countries.get())
            selected_interests = self.get_selected_interests()
            budget = float(self.budget.get())
            home_country = self.starting_country.get()
            start_date = self.start_date.get_date()
            end_date = self.end_date.get_date()
            
            if not all([selected_interests, home_country, num_countries > 0, budget > 0]):
                messagebox.showerror("Input Error", "Please fill in all fields: number of countries, interests, budget, and home country.")
                return

            if start_date >= end_date:
                messagebox.showerror("Date Error", "The start date must be before the end date.")
                return

            selected_countries = self.select_countries(selected_interests, num_countries, home_country)
            
            if not selected_countries:
                messagebox.showwarning("No Matches", "No countries found matching your selected interests. Please try different interests.")
                return
            
            route = self.optimizer.solve_tsp(selected_countries, home_country)
            total_days = (end_date - start_date).days + 1
            days_distribution = self.optimizer.distribute_days(total_days, route, selected_interests)

            # --- NEW: Strict budget check before displaying anything ---
            total_cost = self.calculate_total_cost(route, days_distribution)

            if total_cost > budget:
                messagebox.showwarning(
                    "Budget Exceeded",
                    f"The estimated cost for this trip is ${total_cost:,.2f}, which exceeds your budget of ${budget:,.2f}.\n\n"
                    "Suggestions:\n"
                    " - Increase your budget\n"
                    " - Reduce the number of countries\n"
                    " - Plan a shorter trip (select fewer days)\n"
                    " - Select interests that correspond to cheaper destinations"
                )
                return  # Stop execution here

            # --- If budget is sufficient, proceed to display ---
            self.display_itinerary(route, days_distribution, start_date, budget, home_country)
            self.create_map_visualization(route, days_distribution)

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for 'Number of Countries' and 'Budget'.")
        except Exception as e:
            messagebox.showerror("An Error Occurred", f"An unexpected error occurred: {e}")

    def display_itinerary(self, route: List[str], days_distribution: Dict[str, int], start_dt: datetime.date, budget: float, home_country: str):
        # This method remains the same
        self.result_text.delete(1.0, tk.END)
        total_cost = self.calculate_total_cost(route, days_distribution)
        current_date = start_dt
        self.result_text.insert(tk.END, "=== ✈️ Your Custom Travel Itinerary ===\n\n")
        for country in route[1:-1]:
            days = days_distribution.get(country, 1)
            end_date = current_date + timedelta(days=days - 1)
            country_data = self.country_data.countries_data[country]
            self.result_text.insert(tk.END, f"📍 {country.upper()}\n")
            self.result_text.insert(tk.END, f"   - Duration: {days} days ({current_date.strftime('%b %d')} - {end_date.strftime('%b %d')})\n")
            self.result_text.insert(tk.END, f"   - Est. Accommodation: ${country_data['avg_accommodation_cost']*days:,}\n")
            self.result_text.insert(tk.END, f"   - Est. Travel Cost to here: ${country_data['avg_travel_cost']:,}\n")
            self.result_text.insert(tk.END, f"   - Main Interests: {', '.join(country_data['interests'])}\n\n")
            current_date = end_date + timedelta(days=1)
        self.result_text.insert(tk.END, f"🏠 Return to {home_country}\n")
        if len(route) > 2:
            self.result_text.insert(tk.END, f"   - Est. Return Travel Cost: ${self.country_data.countries_data[route[-2]]['avg_travel_cost']:,}\n\n")
        self.result_text.insert(tk.END, "--- Route Summary ---\n")
        self.result_text.insert(tk.END, f"🗺️ Route: {' → '.join(route)}\n\n")
        self.result_text.insert(tk.END, "--- Financial Summary ---\n")
        self.result_text.insert(tk.END, f"💰 Total Estimated Cost: ${total_cost:,.2f}\n")
        self.result_text.insert(tk.END, f"💵 Your Budget: ${budget:,.2f}\n")
        remaining_budget = budget - total_cost
        self.result_text.insert(tk.END, f"✅ Remaining Budget: ${remaining_budget:,.2f}\n")
        self.result_text.insert(tk.END, "\nMap of your journey has been generated and opened in your browser.")
    
    def create_map_visualization(self, route: List[str], days_distribution: Dict[str, int]):
        # This method remains the same
        if not route: return
        coords = [tuple(self.country_data.countries_data[country]["coordinates"]) for country in route]
        avg_lat = sum(p[0] for p in coords) / len(coords)
        avg_lon = sum(p[1] for p in coords) / len(coords)
        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=2)
        for i, country in enumerate(route):
            location = coords[i]
            if i == 0:
                popup_text = f"🏠 Start & End: {country}"
                icon = folium.Icon(color='green', icon='home')
            else:
                if country == route[-1]: continue
                days = days_distribution.get(country, 'N/A')
                popup_text = f"📍 {i}. {country} ({days} days)"
                icon = folium.Icon(color='blue', icon='info-sign')
            folium.Marker(location=location, popup=popup_text, icon=icon).add_to(m)
        folium.PolyLine(coords, color="red", weight=2.5, opacity=1).add_to(m)
        map_file = "tour_map.html"
        m.save(map_file)
        webbrowser.open('file://' + os.path.realpath(map_file))

# --- Main Application Execution ---
if __name__ == "__main__":
    if not country_data:
        print("Failed to load country data. Exiting application.")
    else:
        root = tk.Tk()
        root.geometry("1200x750")
        app = TourPlannerGUI(root)
        root.mainloop()