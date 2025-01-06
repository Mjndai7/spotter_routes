# spotter_routes

The Route Planner API calculates an optimal driving route between two locations within the USA and provides cost-effective fuel stop recommendations based on fuel prices. The API returns key information about the route, fuel consumption, stops needed, and total fuel cost.

Features

Route Generation: Calculates a route using OpenRouteService API with the start and finish locations provided.
Fuel Stop Optimization: Identifies the most cost-effective fuel stations along the route based on the latest fuel prices.
Fuel Consumption: Estimates total fuel required, given a vehicle achieves 10 miles per gallon.
Cost Estimation: Provides the total estimated cost of fuel for the trip.
Dynamic Routing: Handles routes with multiple fuel stops if the trip exceeds the vehicle's 500-mile range.
