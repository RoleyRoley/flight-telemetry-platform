import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";

import L from "leaflet";
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

export default function MapView() {
    const [telemetry, setTelemetry] = useState(null);

    useEffect(() => {
        async function fetchLatestTelemetry() {
            const response = await fetch('http://localhost:8000/telemetry/latest');
            const data = await response.json();
            setTelemetry(data);
            // Log the latest telemetry data to the console for debugging
            console.log("Latest telemetry:", data);
        }

        fetchLatestTelemetry();

        const interval = setInterval(fetchLatestTelemetry, 2000); // Fetch every 5 seconds

        return () => clearInterval(interval); // Cleanup on unmount
    }, []);

    const position =
        telemetry?.latitude && telemetry?.longitude
            ? [telemetry.latitude, telemetry.longitude]
            : [51.4700, -0.4543];

    return (

    // Render the map with the latest telemetry data
    <div style={{ height: "100vh", width: "100%" }}>
      <MapContainer center={position} zoom={7} style={{ height: "100%", width: "100%" }}>
        <TileLayer
          attribution="&copy; OpenStreetMap contributors"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {telemetry && (
          <Marker position={position}>
            <Popup>
              <strong>Flight ID:</strong> {telemetry.flight_id}
              <br />
              <strong>Phase:</strong> {telemetry.flight_phase}
              <br />
              <strong>Altitude:</strong> {Math.round(telemetry.altitude_ft)} ft
              <br />
              <strong>Speed:</strong> {Math.round(telemetry.ground_speed_kts)} kts
              <br />
              <strong>Progress:</strong> {telemetry.route_progress_percentage?.toFixed(1)}%
            </Popup>
          </Marker>
        )}
      </MapContainer>
    </div>


    );

}