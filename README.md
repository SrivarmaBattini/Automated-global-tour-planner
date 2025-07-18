# **Automated Global Tour Planner ✈️🌍**

An intelligent desktop application that automatically generates personalized global tour itineraries based on user preferences, travel budget, and interests — complete with an optimized multi-country route and an interactive map.

## **📌 About The Project**

Planning a multi-country international trip can be time-consuming and overwhelming. With so many options, constraints, and preferences, it's difficult to find the perfect itinerary.

The **Automated Global Tour Planner** simplifies this process by using smart heuristics (Nearest Neighbor for TSP), interest-based country selection, and budget-aware logic to generate a complete travel plan in seconds. All routes are visualized using an interactive Folium map.

---

## **✨ Key Features**

- **🔍 Personalized Itinerary Generation**  
  Tailors travel plans based on interests, number of countries, and travel dates.

- **🧠 Interest-Based Country Selection**  
  Dynamically picks countries matching selected interests from a diverse dataset.

- **💰 Budget-Conscious Travel**  
  Estimates accommodation and travel costs per country and alerts if the trip exceeds the budget.

- **📍 TSP Route Optimization**  
  Solves a simplified Traveling Salesperson Problem using the **Nearest Neighbor algorithm** to find the shortest route visiting all selected countries.

- **📅 Smart Day Distribution**  
  Distributes days across countries proportionally based on interest match scores.

- **🗺️ Interactive Map Visualization**  
  Creates an HTML map showing the travel route using **Folium**, auto-opens in browser.

---

## **🛠️ Tech Stack**

- **Python** — Core language
- **Tkinter** — GUI for travel inputs and itinerary output
- **Folium** — Map generation
- **NumPy** — Distance computation
- **tkcalendar** — Start/End date entry widgets
- **JSON** — Used to store travel data (`data.json`)

---

## **🌍 Countries Supported**

The app supports **25 countries** across multiple continents, each with:
- Coordinates (for mapping and distance calculation)
- List of travel interests (e.g., culture, wildlife, adventure)
- Average travel and accommodation costs

See `data.json` for the complete list.

---
