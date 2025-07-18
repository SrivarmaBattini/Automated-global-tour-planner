# ✈️🌍 Automated Global Tour Planner

A smart Python-based desktop application that generates optimized multi-country travel itineraries based on user preferences such as interests, duration, budget, and starting location. The system uses heuristic search (TSP via Nearest Neighbor) and interest-matching logic to deliver a personalized travel plan and an interactive route map.

---

## 📌 About The Project

Planning a multi-country international trip is complex due to constraints like budget, time, and personal preferences. Manually optimizing the itinerary is time-consuming and often inefficient.

The **Automated Global Tour Planner** applies core AI techniques to solve this problem:
- Heuristic routing (Nearest Neighbor TSP)
- Constraint satisfaction (budget, time, preferences)
- Interest-based filtering
- Personalized planning logic

This tool provides an intuitive GUI to collect inputs and outputs a complete travel plan with dates, costs, and routes — all visualized on an interactive map.

---


## 🚀 Key Features

- **🧠 Intelligent Country Selection**  
  Picks countries that align best with the user's travel interests.

- **📍 Optimized Route Planning**  
  Solves TSP using Nearest Neighbor to minimize travel distances between countries.

- **📅 Smart Day Allocation**  
  Distributes total trip days proportionally based on interest overlap.

- **💰 Budget-Conscious Itinerary**  
  Estimates total cost and warns if the trip exceeds the user's budget.

- **🗺️ Map Visualization**  
  Interactive HTML map with markers for each destination and red polyline for the route.

- **🖥️ User-Friendly Interface**  
  Clean Tkinter GUI with date pickers, combo boxes, and scrollable interest selection.

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **Tkinter** – GUI
- **NumPy** – Distance calculations
- **Folium** – Interactive route maps
- **tkcalendar** – Date inputs
- **JSON** – Country data (`data.json`)

---

## 🌍 Countries Supported

25 predefined countries across multiple continents, each with:
- Travel interests (e.g., adventure, culture, beaches, wildlife)
- Average travel and accommodation costs
- Latitude/longitude coordinates

See [`data.json`](data.json) for details.

---
