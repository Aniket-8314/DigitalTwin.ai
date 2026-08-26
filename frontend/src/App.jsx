import { useEffect, useState } from "react";
import {
  getTwinState,
  getMetrics,
  getStations,
  getVehicles,
  runWhatIf,
  getProcessGraph,
} from "./api/twinApi";
import "./App.css";

function App() {
  const [twinState, setTwinState] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [stations, setStations] = useState([]);
  const [vehicles, setVehicles] = useState([]);
  const [selectedStation, setSelectedStation] = useState(null);
  const [whatIfOpen, setWhatIfOpen] = useState(false);
  const [whatIfStation, setWhatIfStation] = useState(null);
  const [error, setError] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [processGraph, setProcessGraph] =
    useState({
      nodes: [],
      edges: [],
    });
  const openWhatIf = (station) => {
    setWhatIfStation(station);
    setWhatIfOpen(true);
  };

  const buildAlerts = (stationsData, vehiclesData) => {
    const events = [];

    const timestamp = new Date().toLocaleTimeString(
      [],
      {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      }
    );

    stationsData.forEach((station) => {

      if (
        (station.risk_score ?? 0) >= 0.7
      ) {
        events.push({
          id: `${timestamp}-${station.station_id}-risk`,
          time: timestamp,
          station: station.station_id,
          type: "HIGH RISK",
          severity: "critical",
          message:
            `Station risk at ${(
              station.risk_score * 100
            ).toFixed(0)}%`,
        });
      }

      if (
        (station.bottleneck_probability ?? 0) >= 0.7
      ) {
        events.push({
          id: `${timestamp}-${station.station_id}-bottleneck`,
          time: timestamp,
          station: station.station_id,
          type: "BOTTLENECK",
          severity: "warning",
          message:
            `Bottleneck probability ${(
              station.bottleneck_probability *
              100
            ).toFixed(0)
            }%`,
        });
      }

      if (
        (station.anomaly_score ?? 0) >= 0.7
      ) {
        events.push({
          id: `${timestamp}-${station.station_id}-anomaly`,
          time: timestamp,
          station: station.station_id,
          type: "ANOMALY",
          severity: "warning",
          message:
            `Anomaly score ${(
              station.anomaly_score *
              100
            ).toFixed(0)
            }%`,
        });
      }
    });


    vehiclesData.forEach((vehicle) => {

      if (
        (vehicle.defect_probability ?? 0) >= 0.5
      ) {
        events.push({
          id: `${timestamp}-${vehicle.vehicle_id}-defect`,
          time: timestamp,
          station:
            vehicle.current_station,
          type: "QUALITY",
          severity: "critical",
          message:
            `${vehicle.vehicle_id} defect risk ${(
              vehicle.defect_probability *
              100
            ).toFixed(0)
            }%`,
        });
      }
    });

    return events;
  };

  useEffect(() => {
    let intervalId;

    const loadDashboard = async () => {
      try {
        const [
          stateData,
          metricsData,
          stationsData,
          VehiclesData,
          graphData,
        ] = await Promise.all([
          getTwinState(),
          getMetrics(),
          getStations(),
          getVehicles(),
          getProcessGraph(),
        ]);

        setTwinState(stateData);
        setMetrics(metricsData);
        setStations(stationsData);
        setVehicles(VehiclesData);
        setProcessGraph(graphData);
        const newAlerts =
          buildAlerts(
            stationsData,
            VehiclesData
          );

        setAlerts((previous) => {

          const combined = [
            ...newAlerts,
            ...previous,
          ];

          const unique = [];

          const seen = new Set();

          for (const alert of combined) {

            const key =
              `${alert.station}-${alert.type}`;

            if (!seen.has(key)) {

              seen.add(key);

              unique.push(alert);
            }
          }

          return unique.slice(
            0,
            20
          );
        });
        setError(null);
      } catch (err) {
        console.error(
          "Dashboard error:",
          err
        );

        setError(
          "Unable to connect to DigitalTwin backend."
        );
      }
    };

    loadDashboard();


    intervalId = setInterval(
      loadDashboard,
      1000
    );

    return () => {
      clearInterval(intervalId);
    };
  }, []);

  if (error) {
    return (
      <div className="dashboard">
        <div className="error">
          {error}
        </div>
      </div>
    );
  }

  if (!twinState || !metrics) {
    return (
      <div className="dashboard">
        <div className="loading">
          Connecting to DigitalTwin.ai...
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">

      {/* -------------------------------- */}
      {/* Header */}
      {/* -------------------------------- */}

      <div className="system-status-bar">

        <div className="system-status-left">

          <span className="status-pulse" />

          <strong>
            DIGITAL TWIN ONLINE
          </strong>

          <span>
            LIVE SIMULATION
          </span>

        </div>

        <div className="system-status-right">

          <span>
            STEP {twinState?.simulation_step ?? 0}
          </span>

          <span>
            {twinState?.last_updated
              ? new Date(
                twinState.last_updated
              ).toLocaleTimeString()
              : "--:--:--"}
          </span>

        </div>

      </div>

      <header className="topbar">

        <div>
          <h1>DIGITALTWIN.AI</h1>

          <p>
            Intelligent Manufacturing
            Control Center
          </p>
        </div>

        <div className="live-status">

          <span className="live-dot"></span>

          {twinState.is_running
            ? "LIVE"
            : "STOPPED"}

        </div>

      </header>

      <section className="decision-section">

        <div className="section-header">

          <div>

            <h2>
              DECISION INTELLIGENCE
            </h2>

            <p>
              Current highest-priority operational decision
            </p>

          </div>

        </div>


        {stations
          .filter(
            (station) =>
              (station.risk_score ?? 0) > 0
          )
          .sort(
            (a, b) =>
              (b.risk_score ?? 0) -
              (a.risk_score ?? 0)
          )
          .slice(0, 1)
          .map((station) => (

            <div
              className="decision-card"
              key={station.station_id}
            >

              <div className="decision-main">

                <span>
                  PRIORITY STATION
                </span>

                <strong>
                  {station.station_id}
                </strong>

                <p>
                  {station.name}
                </p>

              </div>


              <div className="decision-risk">

                <span>
                  CURRENT RISK
                </span>

                <strong>
                  {(
                    station.risk_score *
                    100
                  ).toFixed(0)}%
                </strong>

              </div>


              <div className="decision-action">

                <span>
                  RECOMMENDED ACTION
                </span>

                <strong>
                  Review station operating
                  conditions
                </strong>

                <button
                  onClick={() =>
                    setSelectedStation(station)
                  }
                >
                  OPEN INTELLIGENCE →
                </button>

              </div>

            </div>

          ))}

      </section>


      {/* -------------------------------- */}
      {/* Metrics */}
      {/* -------------------------------- */}

      <section className="metrics-grid">

        <MetricCard
          title="LINE HEALTH"
          value={`${(
            metrics.line_health * 100
          ).toFixed(1)}%`}
        />

        <MetricCard
          title="AVG CYCLE TIME"
          value={`${metrics.average_cycle_time.toFixed(
            1
          )}s`}
        />

        <MetricCard
          title="THROUGHPUT"
          value={`${metrics.throughput_per_hour.toFixed(
            1
          )}/hr`}
        />

        <MetricCard
          title="BOTTLENECKS"
          value={metrics.bottleneck_count}
        />

      </section>


      {/* -------------------------------- */}
      {/* Factory */}
      {/* -------------------------------- */}

      <section className="factory-section">

        <div className="section-header">

          <div>
            <h2>
              FACTORY OVERVIEW
            </h2>

            <p>
              {stations.length} active
              stations
            </p>
          </div>

          <div className="simulation-info">

            STEP{" "}
            {twinState.simulation_step}

          </div>

        </div>


        <div className="station-grid">

          {stations.map(
            (station) => (
              <StationCard
                key={station.station_id}
                station={station}
                onClick={() =>
                  setSelectedStation(station)
                }
              />
            )
          )}

        </div>

      </section>

      <ProcessGraph
        graph={processGraph}
        stations={stations}
        selectedStation={selectedStation}
        onSelectStation={setSelectedStation}
      />
      <AlertFeed
        alerts={alerts}
      />
      <VehicleIntelligence
        vehicles={vehicles}
      />
      {selectedStation && (
        <StationDetails
          station={
            stations.find(
              (station) =>
                station.station_id ===
                selectedStation.station_id
            ) || selectedStation
          }
          vehicles={vehicles}
          onClose={() =>
            setSelectedStation(null)
          }
          onWhatIf={openWhatIf}
        />
      )}

      {whatIfOpen && whatIfStation && (
        <WhatIfSimulator
          station={whatIfStation}
          onClose={() => {
            setWhatIfOpen(false);
            setWhatIfStation(null);
          }}
        />
      )}

    </div>
  );
}


/* ========================================
   Metric Card
======================================== */

function MetricCard({
  title,
  value,
}) {
  return (
    <div className="metric-card">

      <div className="metric-title">
        {title}
      </div>

      <div className="metric-value">
        {value}
      </div>

    </div>
  );
}


/* ========================================
   Station Card
======================================== */

function StationCard({
  station,
  onClick,
}) {

  const severity =
    station.risk_severity ||
    "low";

  return (
    <div
      className={`station-card ${severity}`}
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={(event) => {
        if (event.key === "Enter") {
          onClick();
        }
      }}
    >

      <div className="station-header">

        <strong>
          {station.station_id}
        </strong>

        <span className="severity">
          {severity.toUpperCase()}
        </span>

      </div>


      <div className="station-name">
        {station.name}
      </div>


      <div className="station-data">

        <div>
          <span>
            Cycle
          </span>

          <strong>
            {station.cycle_time.toFixed(
              1
            )}s
          </strong>
        </div>


        <div>
          <span>
            Queue
          </span>

          <strong>
            {station.queue_length}
          </strong>
        </div>


        <div>
          <span>
            Risk
          </span>

          <strong>
            {(
              station.risk_score * 100
            ).toFixed(0)}
            %
          </strong>
        </div>

      </div>


      <div className="risk-bar">

        <div
          className="risk-fill"
          style={{
            width: `${station.risk_score * 100
              }%`,
          }}
        />

      </div>

    </div>
  );
}


function StationDetails({
  station,
  vehicles,
  onClose,
  onWhatIf,
}) {
  const affectedVehicles =
    vehicles.filter(
      (vehicle) =>
        vehicle.current_station ===
        station.station_id ||
        vehicle.defect_origin ===
        station.station_id
    );

  const highRiskAffectedVehicles =
    affectedVehicles.filter(
      (vehicle) =>
        (vehicle.defect_probability ?? 0) >=
        0.5
    );
  const riskPercent =
    station.risk_score * 100;

  return (
    <div className="station-overlay">

      <div className="station-details">

        {/* Header */}

        <div className="details-header">

          <div>
            <span className="details-label">
              STATION
            </span>

            <h2>
              {station.station_id}
            </h2>

            <p>
              {station.name}
            </p>
          </div>

          <button
            className="close-button"
            onClick={onClose}
          >
            ×
          </button>

        </div>


        {/* Risk */}

        <div className="details-risk">

          <div>
            <span>
              CURRENT RISK
            </span>

            <strong>
              {riskPercent.toFixed(0)}%
            </strong>
          </div>

          <div
            className={`details-severity ${station.risk_severity}`}
          >
            {station.risk_severity?.toUpperCase()}
          </div>

        </div>


        {/* Risk Intelligence */}

        <div className="risk-intelligence">

          <div className="risk-intelligence-header">

            <div>
              <span>
                RISK INTELLIGENCE
              </span>

              <h3>
                Current Station Risk
              </h3>
            </div>

            <strong>
              {(
                station.risk_score * 100
              ).toFixed(0)}%
            </strong>

          </div>


          {/* Overall risk */}

          <div className="overall-risk-bar">

            <div
              className={`overall-risk-fill ${station.risk_severity}`}
              style={{
                width: `${station.risk_score * 100
                  }%`,
              }}
            />

          </div>


          {/* AI indicators */}

          <div className="ai-grid">

            <Indicator
              label="ANOMALY"
              value={
                station.anomaly_score
              }
            />

            <Indicator
              label="BOTTLENECK"
              value={
                station.bottleneck_probability
              }
            />

            <Indicator
              label="HEALTH"
              value={
                station.health
              }
            />

          </div>

        </div>


        {/* Telemetry */}

        <div className="details-section">

          <h3>
            LIVE TELEMETRY
          </h3>

          <div className="telemetry-grid">

            <TelemetryItem
              label="Cycle Time"
              value={`${station.cycle_time.toFixed(
                2
              )} s`}
            />

            <TelemetryItem
              label="Takt Time"
              value={`${station.takt_time.toFixed(
                2
              )} s`}
            />

            <TelemetryItem
              label="Torque"
              value={station.torque.toFixed(2)}
            />

            <TelemetryItem
              label="Vibration"
              value={station.vibration.toFixed(
                3
              )}
            />

            <TelemetryItem
              label="Temperature"
              value={`${station.temperature.toFixed(
                2
              )} °C`}
            />

            <TelemetryItem
              label="Queue"
              value={station.queue_length}
            />

          </div>

        </div>


        {/* Root Cause Intelligence */}

        <div className="details-section root-cause-section">

          <div className="details-section-heading">

            <div>
              <h3>
                ROOT CAUSE INTELLIGENCE
              </h3>

              <p>
                Signals contributing to current station risk
              </p>
            </div>

            <span className="cause-count">
              {station.root_causes?.length || 0}
              {" "}SIGNALS
            </span>

          </div>


          {station.root_causes?.length ? (

            <div className="cause-list">

              {station.root_causes.map(
                (cause, index) => {

                  const score =
                    Math.max(
                      0,
                      Math.min(
                        1,
                        cause.score ?? 0
                      )
                    );

                  return (
                    <div
                      className="cause-item"
                      key={`${cause.signal}-${index}`}
                    >

                      <div className="cause-content">

                        <div className="cause-title">

                          <div>
                            <strong>
                              {cause.signal}
                            </strong>

                            <small>
                              {cause.evidence}
                            </small>
                          </div>

                          <span>
                            {(score * 100).toFixed(0)}%
                          </span>

                        </div>


                        <div className="cause-bar">

                          <div
                            style={{
                              width:
                                `${score * 100}%`,
                            }}
                          />

                        </div>

                      </div>

                    </div>
                  );
                }
              )}

            </div>

          ) : (

            <p className="empty-state">
              No significant root causes detected.
            </p>

          )}

        </div>

        {station.root_causes?.length > 0 && (
          <div className="causal-summary">

            <div className="causal-icon">
              AI
            </div>

            <div>

              <strong>
                Primary driver identified
              </strong>

              <p>
                {station.root_causes[0].signal}
                {" "}is currently the strongest
                contributing signal.
              </p>

            </div>

          </div>
        )}

        <div className="details-section">

          <div className="details-section-heading">

            <div>

              <h3>
                IMPACTED VEHICLES
              </h3>

              <p>
                Vehicles currently associated with this station
              </p>

            </div>

            <span className="cause-count">
              {highRiskAffectedVehicles.length}
              {" "}HIGH RISK
            </span>

          </div>


          {affectedVehicles.length > 0 ? (

            <div className="affected-vehicle-list">

              {affectedVehicles.map(
                (vehicle) => {

                  const probability =
                    vehicle.defect_probability ?? 0;

                  const severity =
                    vehicle.defect_severity ||
                    "low";

                  return (
                    <div
                      className="affected-vehicle"
                      key={vehicle.vehicle_id}
                    >

                      <div>

                        <strong>
                          {vehicle.vehicle_id}
                        </strong>

                        <span>
                          Quality{" "}
                          {(
                            (vehicle.quality_score ?? 0) *
                            100
                          ).toFixed(0)}%
                        </span>

                      </div>


                      <div className="affected-vehicle-risk">

                        <span>
                          {(probability * 100).toFixed(0)}%
                        </span>

                        <span
                          className={
                            `vehicle-status ${severity}`
                          }
                        >
                          {severity.toUpperCase()}
                        </span>

                      </div>

                    </div>
                  );
                }
              )}

            </div>

          ) : (

            <p className="empty-state">
              No vehicles currently impacted.
            </p>

          )}

        </div>


        {/* AI Recommendations */}

        <div className="details-section recommendation-section">

          <div className="details-section-heading">

            <div>

              <h3>
                AI RECOMMENDATIONS
              </h3>

              <p>
                Recommended interventions based on current
                station conditions
              </p>

            </div>

            <span className="cause-count">
              {station.recommendations?.length || 0}
              {" "}ACTIONS
            </span>

          </div>


          {station.recommendations?.length ? (

            <div className="recommendation-list">

              {station.recommendations.map(
                (recommendation, index) => {

                  const confidence = Math.max(
                    0,
                    Math.min(
                      1,
                      recommendation.confidence ?? 0
                    )
                  );

                  const priority =
                    recommendation.priority ||
                    "medium";

                  return (
                    <div
                      className={
                        `recommendation-item ${priority}`
                      }
                      key={index}
                    >

                      <div className="recommendation-top">

                        <span>
                          {priority.toUpperCase()}
                        </span>

                        <span>
                          CONFIDENCE{" "}
                          {(confidence * 100).toFixed(0)}%
                        </span>

                      </div>


                      <strong className="recommendation-action">
                        {recommendation.action}
                      </strong>


                      <p>
                        {recommendation.reason}
                      </p>


                      <div className="recommendation-effect">

                        <span>
                          EXPECTED EFFECT
                        </span>

                        <strong>
                          {recommendation.expected_effect}
                        </strong>

                      </div>


                      <div className="confidence-bar">

                        <div
                          style={{
                            width:
                              `${confidence * 100}%`,
                          }}
                        />

                      </div>


                      <button
                        className="what-if-button"
                        onClick={() => {
                          onWhatIf(station);
                        }}
                      >
                        TEST WITH WHAT-IF →
                      </button>

                    </div>
                  );
                }
              )}

            </div>

          ) : (

            <p className="empty-state">
              No recommendations available for the
              current station state.
            </p>

          )}

        </div>

      </div>

    </div>
  );
}

function QualityValue({
  value,
}) {
  const percentage =
    Math.max(
      0,
      Math.min(
        100,
        value * 100
      )
    );

  let level = "good";

  if (percentage < 70) {
    level = "critical";
  } else if (percentage < 85) {
    level = "warning";
  }

  return (
    <div className="quality-value">

      <span>
        {percentage.toFixed(0)}%
      </span>

      <div className="quality-bar">

        <div
          className={level}
          style={{
            width: `${percentage}%`,
          }}
        />

      </div>

    </div>
  );
}

function AlertFeed({
  alerts,
}) {
  return (
    <section className="alerts-section">

      <div className="section-header">

        <div>

          <h2>
            LIVE EVENT FEED
          </h2>

          <p>
            Real-time events generated by the
            digital twin
          </p>

        </div>

        <span className="live-indicator">
          <i />
          LIVE
        </span>

      </div>


      {alerts.length === 0 ? (

        <div className="empty-alerts">
          No active events detected.
        </div>

      ) : (

        <div className="alert-list">

          {alerts.map((alert) => (

            <div
              className={
                `alert-item ${alert.severity}`
              }
              key={alert.id}
            >

              <div className="alert-time">
                {alert.time}
              </div>

              <div className="alert-indicator">
                <span />
              </div>

              <div className="alert-content">

                <div className="alert-title">

                  <strong>
                    {alert.station}
                  </strong>

                  <span>
                    {alert.type}
                  </span>

                </div>

                <p>
                  {alert.message}
                </p>

              </div>

            </div>

          ))}

        </div>

      )}

    </section>
  );
}

function VehicleIntelligence({
  vehicles,
}) {
  const highRiskVehicles =
    vehicles
      .filter(
        (vehicle) =>
          vehicle.defect_probability >= 0.5
      )
      .sort(
        (a, b) =>
          b.defect_probability -
          a.defect_probability
      );

  const defectOriginCounts =
    vehicles.reduce(
      (counts, vehicle) => {
        if (vehicle.defect_origin) {
          counts[vehicle.defect_origin] =
            (counts[vehicle.defect_origin] || 0) +
            1;
        }

        return counts;
      },
      {}
    );

  const topOrigin = Object.entries(
    defectOriginCounts
  ).sort(
    (a, b) => b[1] - a[1]
  )[0];

  return (
    <section className="vehicle-section">

      <div className="section-header">

        <div>
          <h2>
            VEHICLE & DEFECT INTELLIGENCE
          </h2>

          <p>
            AI-predicted quality risk across
            vehicles
          </p>
        </div>

        <div className="vehicle-summary">

          <strong>
            {highRiskVehicles.length}
          </strong>

          <span>
            HIGH RISK
          </span>

        </div>

      </div>


      {/* Summary */}

      <div className="vehicle-summary-grid">

        <div className="vehicle-stat">

          <span>
            VEHICLES
          </span>

          <strong>
            {vehicles.length}
          </strong>

        </div>


        <div className="vehicle-stat">

          <span>
            HIGH RISK
          </span>

          <strong>
            {highRiskVehicles.length}
          </strong>

        </div>


        <div className="vehicle-stat">

          <span>
            TOP DEFECT ORIGIN
          </span>

          <strong>
            {topOrigin
              ? topOrigin[0]
              : "—"}
          </strong>

        </div>


        <div className="vehicle-stat">

          <span>
            DEFECT ORIGIN COUNT
          </span>

          <strong>
            {topOrigin
              ? topOrigin[1]
              : 0}
          </strong>

        </div>

      </div>


      {/* Vehicle table */}

      <div className="vehicle-table-wrapper">

        <table className="vehicle-table">

          <thead>

            <tr>
              <th>VEHICLE</th>
              <th>STATION</th>
              <th>QUALITY</th>
              <th>DEFECT RISK</th>
              <th>ORIGIN</th>
              <th>STATUS</th>
            </tr>

          </thead>

          <tbody>

            {vehicles.map(
              (vehicle) => {

                const probability =
                  vehicle.defect_probability ?? 0;

                const severity =
                  vehicle.defect_severity ||
                  "low";

                return (
                  <tr
                    key={vehicle.vehicle_id}
                  >

                    <td>
                      <strong>
                        {vehicle.vehicle_id}
                      </strong>
                    </td>

                    <td>
                      {vehicle.current_station}
                    </td>

                    <td>
                      <QualityValue
                        value={
                          vehicle.quality_score
                        }
                      />
                    </td>

                    <td>

                      <div className="vehicle-risk">

                        <span>
                          {(
                            probability * 100
                          ).toFixed(0)}%
                        </span>

                        <div className="vehicle-risk-bar">

                          <div
                            className={
                              `vehicle-risk-fill ${severity}`
                            }
                            style={{
                              width:
                                `${probability * 100}%`,
                            }}
                          />

                        </div>

                      </div>

                    </td>

                    <td>
                      {vehicle.defect_origin ||
                        "—"}
                    </td>

                    <td>

                      <span
                        className={
                          `vehicle-status ${severity}`
                        }
                      >
                        {severity.toUpperCase()}
                      </span>

                    </td>

                  </tr>
                );
              }
            )}

          </tbody>

        </table>

      </div>

    </section>
  );
}

function Indicator({
  label,
  value,
}) {
  const percentage =
    Math.max(
      0,
      Math.min(
        100,
        value * 100
      )
    );

  let level = "LOW";

  if (percentage >= 70) {
    level = "HIGH";
  } else if (percentage >= 40) {
    level = "MEDIUM";
  }

  if (label === "HEALTH") {
    if (percentage >= 70) {
      level = "GOOD";
    } else if (percentage >= 40) {
      level = "WARNING";
    } else {
      level = "CRITICAL";
    }
  }

  return (
    <div className="indicator">

      <div className="indicator-header">

        <span>
          {label}
        </span>

        <small>
          {level}
        </small>

      </div>

      <strong>
        {percentage.toFixed(0)}%
      </strong>

      <div className="indicator-bar">

        <div
          className={`indicator-fill ${level.toLowerCase()}`}
          style={{
            width: `${percentage}%`,
          }}
        />

      </div>

    </div>
  );
}

function TelemetryItem({
  label,
  value,
}) {
  return (
    <div className="telemetry-item">

      <span>
        {label}
      </span>

      <strong>
        {value}
      </strong>

    </div>
  );
}

function ScenarioSlider({
  label,
  value,
  min,
  max,
  step,
  unit,
  onChange,
}) {
  return (
    <div className="scenario-slider">

      <div className="scenario-slider-header">

        <span>
          {label}
        </span>

        <strong>
          {value}
          {unit}
        </strong>

      </div>

      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(event) =>
          onChange(event.target.value)
        }
      />

      <div className="slider-range">

        <span>
          {min}
          {unit}
        </span>

        <span>
          {max}
          {unit}
        </span>

      </div>

    </div>
  );
}

function WhatIfSimulator({
  station,
  onClose,
}) {
  const [scenario, setScenario] =
    useState({
      station_id: station.station_id,
      speed_change_percent: 0,
      queue_change: 0,
      temperature_change: 0,
      vibration_change: 0,
      torque_change: 0,
    });

  const [result, setResult] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState(null);

  const updateScenario = (
    field,
    value
  ) => {
    setScenario((previous) => ({
      ...previous,
      [field]: Number(value),
    }));
  };

  const simulate = async () => {
    try {
      setLoading(true);
      setError(null);

      const data =
        await runWhatIf(scenario);

      setResult(data);
    } catch (err) {
      console.error(
        "What-if error:",
        err
      );

      setError(
        err.response?.data?.detail ||
        err.message ||
        "Unable to run simulation."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="what-if-overlay">

      <div className="what-if-panel">

        {/* Header */}

        <div className="what-if-header">

          <div>

            <span>
              DIGITAL TWIN SIMULATION
            </span>

            <h2>
              WHAT-IF ANALYSIS
            </h2>

            <p>
              Simulate an intervention before
              applying it to production.
            </p>

          </div>

          <button
            className="close-button"
            onClick={onClose}
          >
            ×
          </button>

        </div>


        {/* Scenario */}

        <div className="what-if-section">

          <h3>
            SCENARIO
          </h3>


          <div className="scenario-station">

            <span>
              TARGET STATION
            </span>

            <strong>
              {station.station_id}
            </strong>

          </div>


          <ScenarioSlider
            label="Speed Change"
            value={
              scenario.speed_change_percent
            }
            min={-10}
            max={10}
            step={1}
            unit="%"
            onChange={(value) =>
              updateScenario(
                "speed_change_percent",
                value
              )
            }
          />


          <ScenarioSlider
            label="Queue Change"
            value={
              scenario.queue_change
            }
            min={-5}
            max={5}
            step={1}
            unit=""
            onChange={(value) =>
              updateScenario(
                "queue_change",
                value
              )
            }
          />


          <ScenarioSlider
            label="Temperature Change"
            value={
              scenario.temperature_change
            }
            min={-10}
            max={10}
            step={0.5}
            unit="°C"
            onChange={(value) =>
              updateScenario(
                "temperature_change",
                value
              )
            }
          />


          <ScenarioSlider
            label="Vibration Change"
            value={
              scenario.vibration_change
            }
            min={-0.5}
            max={0.5}
            step={0.01}
            unit=""
            onChange={(value) =>
              updateScenario(
                "vibration_change",
                value
              )
            }
          />


          <ScenarioSlider
            label="Torque Change"
            value={
              scenario.torque_change
            }
            min={-5}
            max={5}
            step={0.1}
            unit=""
            onChange={(value) =>
              updateScenario(
                "torque_change",
                value
              )
            }
          />


          <button
            className="simulate-button"
            onClick={simulate}
            disabled={loading}
          >
            {loading
              ? "SIMULATING..."
              : "RUN SIMULATION"}
          </button>


          {error && (
            <div className="what-if-error">
              {error}
            </div>
          )}

        </div>


        {/* Results */}

        {result && (
          <WhatIfResults
            result={result}
          />
        )}

      </div>

    </div>
  );
}

function WhatIfResults({
  result,
}) {
  const riskChange =
    result.risk_change;

  const riskImproved =
    riskChange < 0;

  return (
    <div className="what-if-results">

      <div className="what-if-result-header">

        <div>
          <span>
            SIMULATION RESULT
          </span>

          <h3>
            {result.verdict
              .replaceAll(
                "_",
                " "
              )
              .toUpperCase()}
          </h3>
        </div>

        <strong
          className={
            riskImproved
              ? "risk-improved"
              : "risk-increased"
          }
        >
          {riskImproved
            ? "↓"
            : "↑"}{" "}
          {Math.abs(
            riskChange * 100
          ).toFixed(1)}
          pts
        </strong>

      </div>


      {/* Risk */}

      <div className="what-if-risk">

        <div>

          <span>
            BASELINE RISK
          </span>

          <strong>
            {(
              result.baseline.risk *
              100
            ).toFixed(1)}%
          </strong>

        </div>

        <div className="risk-arrow">
          →
        </div>

        <div>

          <span>
            SIMULATED RISK
          </span>

          <strong>
            {(
              result.simulation.risk *
              100
            ).toFixed(1)}%
          </strong>

        </div>

      </div>


      {/* Comparison */}

      <div className="what-if-comparison">

        <ComparisonRow
          label="Cycle Time"
          baseline={
            result.baseline.cycle_time
          }
          simulated={
            result.simulation.cycle_time
          }
          suffix="s"
        />

        <ComparisonRow
          label="Queue"
          baseline={
            result.baseline.queue
          }
          simulated={
            result.simulation.queue
          }
          suffix=""
        />

        <ComparisonRow
          label="Temperature"
          baseline={
            result.baseline.temperature
          }
          simulated={
            result.simulation.temperature
          }
          suffix="°C"
        />

        <ComparisonRow
          label="Vibration"
          baseline={
            result.baseline.vibration
          }
          simulated={
            result.simulation.vibration
          }
          suffix=""
        />

        <ComparisonRow
          label="Torque"
          baseline={
            result.baseline.torque
          }
          simulated={
            result.simulation.torque
          }
          suffix=""
        />

      </div>


      {/* Downstream */}

      <div className="downstream-section">

        <h3>
          DOWNSTREAM IMPACT
        </h3>

        {result.downstream_impact?.map(
          (impact) => {

            const healthChange =
              impact.simulated_health -
              impact.baseline_health;

            return (
              <div
                className="downstream-row"
                key={impact.station_id}
              >

                <strong>
                  {impact.station_id}
                </strong>

                <span>
                  Cycle{" "}
                  {impact.baseline_cycle_time.toFixed(
                    1
                  )}
                  {" → "}
                  {impact.simulated_cycle_time.toFixed(
                    1
                  )}s
                </span>

                <span
                  className={
                    healthChange < 0
                      ? "health-down"
                      : "health-up"
                  }
                >
                  Health{" "}
                  {(
                    impact.baseline_health *
                    100
                  ).toFixed(1)}
                  %
                  {" → "}
                  {(
                    impact.simulated_health *
                    100
                  ).toFixed(1)}
                  %
                </span>

              </div>
            );
          }
        )}

      </div>

    </div>
  );
}


function ComparisonRow({
  label,
  baseline,
  simulated,
  suffix,
}) {
  const change =
    simulated - baseline;

  return (
    <div className="comparison-row">

      <span>
        {label}
      </span>

      <strong>
        {baseline.toFixed
          ? baseline.toFixed(2)
          : baseline}
        {suffix}
      </strong>

      <span>
        →
      </span>

      <strong>
        {simulated.toFixed
          ? simulated.toFixed(2)
          : simulated}
        {suffix}
      </strong>

      <small
        className={
          change <= 0
            ? "change-negative"
            : "change-positive"
        }
      >
        {change >= 0
          ? "+"
          : ""}
        {change.toFixed
          ? change.toFixed(2)
          : change}
        {suffix}
      </small>

    </div>
  );
}

function ProcessGraph({
  graph,
  stations,
  selectedStation,
  onSelectStation,
}) {
  const stationMap = new Map(
    stations.map(
      (station) => [
        station.station_id,
        station,
      ]
    )
  );

  const stationNodes =
    (graph?.nodes || []).filter(
      (node) =>
        typeof node.id === "string" &&
        node.id.startsWith("S")
    );

  return (
    <section className="process-section">

      <div className="section-header">

        <div>

          <h2>
            DIGITAL FACTORY FLOW
          </h2>

          <p>
            Live production topology and risk propagation
          </p>

        </div>

        <div className="process-legend">

          <span>
            <i className="legend-dot healthy" />
            HEALTHY
          </span>

          <span>
            <i className="legend-dot warning" />
            WARNING
          </span>

          <span>
            <i className="legend-dot critical" />
            HIGH RISK
          </span>

        </div>

      </div>


      <div className="process-graph">

        {stationNodes.map(
          (node, index) => {

            const station =
              stationMap.get(
                node.id
              );

            if (!station) {
              return null;
            }

            const risk =
              station.risk_score ?? 0;

            let status =
              "healthy";

            if (risk >= 0.7) {
              status = "critical";
            } else if (risk >= 0.4) {
              status = "warning";
            }

            const selected =
              selectedStation?.station_id ===
              station.station_id;

            return (
              <div
                className="process-node-wrapper"
                key={node.id}
              >

                <button
                  className={
                    `process-node ${status} ${selected
                      ? "selected"
                      : ""
                    }`
                  }
                  onClick={() =>
                    onSelectStation(station)
                  }
                >

                  <span className="node-id">
                    {station.station_id}
                  </span>

                  <span className="node-risk">
                    {(
                      risk * 100
                    ).toFixed(0)}%
                  </span>

                  <span className="node-name">
                    {station.name}
                  </span>

                </button>


                {index <
                  stationNodes.length - 1 && (
                    <div className="process-arrow">
                      →
                    </div>
                  )}

              </div>
            );
          }
        )}

      </div>

    </section>
  );
}

export default App;