# **Automated Global Tour Planner ✈️🌍**

An interactive desktop application that automatically generates personalized global tour itineraries based on user preferences, budget, and interests, complete with an optimized travel route visualized on an interactive map.

A preview of the Tour Planner interface.

## **📌 About The Project**

Planning an international trip is a complex task with multiple constraints like budget, time, and personal interests. Manually optimizing routes and schedules is often tedious and inefficient.

The **Automated Global Tour Planner** solves this by providing a smart, user-friendly tool that automates the entire process. Users can input their travel preferences, and the application generates a complete, optimized itinerary, saving time and effort while creating the perfect trip.

### **Key Features**

* **✨** Personalized Itinerary **Generation**: Creates custom travel plans based on user-defined criteria.  
* **🧠 Interest-Based Filtering**: Intelligently selects countries that best match the user's chosen travel interests (e.g., Adventure, Culture, Beaches).  
* **💰 Budget-Aware Planning**: Ensures the generated itinerary's estimated cost does not exceed the user's specified budget. It provides clear warnings and suggestions if the budget is insufficient.  
* **🗺️** Optimized Route **Planning**: Implements the **Nearest Neighbor algorithm** to solve the Traveling Salesperson Problem (TSP), ensuring an efficient travel path between the selected countries.  
* **📅 Dynamic Day Distribution**: Allocates the total trip duration among destinations proportionally, assigning more time to places that align with the user's interests.  
* **🌐 Interactive Map Visualization**: Generates and automatically opens an interactive HTML map using **Folium** that plots the entire travel route with markers for each destination.

### **🛠️ Built With**

* **Python**: Core programming language.  
* **Tkinter**: For the graphical user interface (GUI).  
* **Folium**: To create interactive Leaflet maps.  
* **Numpy**: For numerical operations and distance calculations.  
* **tkcalendar**: For a user-friendly date entry widget.

## **🚀 Getting Started**

To get a local copy up and running, follow these simple steps.

### **Prerequisites**

Make sure you have Python 3 installed on your system.

### **Installation**

1. **Clone the repository:**  
   git clone \[https://github.com/kbruhadesh/Automated-Global-Tour-Planner-.git\](https://github.com/kbruhadesh/Automated-Global-Tour-Planner-.git)  
   cd Automated-Global-Tour-Planner-

2. **Create and activate a virtual environment (recommended):**  
   \# For macOS/Linux  
   python3 \-m venv venv  
   source venv/bin/activate

   \# For Windows  
   python \-m venv venv  
   venv\\Scripts\\activate

3. **Install the required libraries:**  
   pip install \-r requirements.txt

   *(If a requirements.txt file is not available, install packages manually):*  
   pip install numpy tkcalendar folium

### **Running the Application**

Once the setup is complete, run the main script from your terminal:

python TourPlanner.py

## **📖 Usage**

1. Launch the application.  
2. Fill in the **"Travel Parameters"** on the left:  
   * Enter the **Number of Countries** you wish to visit.  
   * Select your **Travel Interests** from the checklist.  
   * Choose your **Start** and **End Dates**.  
   * Enter your total **Budget (USD)**.  
   * Select your **Home Country** from the dropdown.  
3. Click the **"Generate Itinerary & Map 🗺️"** button.  
4. The application will process your request:  
   * If the trip is feasible within your budget, a detailed **Travel Itinerary** will appear on the right, and an interactive map (tour\_map.html) will open in your web browser.  
   * If the trip exceeds your budget, a warning message will appear with helpful suggestions.

\!\[GIF of Usage\](