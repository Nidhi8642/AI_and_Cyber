import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [summary, setSummary] = useState({
    total_events: 0,
    open_alerts: 0,
    critical_alerts: 0,
    ml_anomalies: 0,
  });

  const [loading, setLoading] = useState(true);
  const [alerts, setAlerts] = useState([]);
  const [events, setEvents] = useState([]);

  // Navigation
  const [activePage, setActivePage] = useState("Dashboard");

  // Alert filters
  const [alertSeverity, setAlertSeverity] = useState("all");

  // Event filters
  const [eventSeverity, setEventSeverity] = useState("all");
  const [eventType, setEventType] = useState("all");

  // AI Assistant
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [aiAnalysis, setAiAnalysis] = useState(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState("");

  // ===========================================
  // Filter Alerts
  // ===========================================

  const filteredAlerts = alerts.filter((alert) => {
    return (
      alertSeverity === "all" ||
      alert.severity === alertSeverity
    );
  });

  // ===========================================
  // Filter Events
  // ===========================================

  const filteredEvents = events.filter((event) => {
    const matchesSeverity =
      eventSeverity === "all" ||
      event.severity === eventSeverity;

    const matchesType =
      eventType === "all" ||
      event.event_type === eventType;

    return matchesSeverity && matchesType;
  });

  // ===========================================
  // Fetch Dashboard Data
  // ===========================================

  useEffect(() => {
    Promise.all([
      fetch(`${API_URL}/dashboard/summary`),
      fetch(`${API_URL}/dashboard/alerts`),
      fetch(`${API_URL}/dashboard/events`),
    ])
      .then(
        async ([
          summaryResponse,
          alertsResponse,
          eventsResponse,
        ]) => {
          const summaryData =
            await summaryResponse.json();

          const alertsData =
            await alertsResponse.json();

          const eventsData =
            await eventsResponse.json();

          setSummary(summaryData);
          setAlerts(alertsData);
          setEvents(eventsData);
          setLoading(false);
        }
      )
      .catch((error) => {
        console.error(
          "Failed to fetch dashboard data:",
          error
        );

        setLoading(false);
      });
  }, []);

  // ===========================================
  // Analytics
  // ===========================================

  const eventSeverityCounts = {
    critical: events.filter(
      (event) => event.severity === "critical"
    ).length,

    high: events.filter(
      (event) => event.severity === "high"
    ).length,

    medium: events.filter(
      (event) => event.severity === "medium"
    ).length,

    low: events.filter(
      (event) => event.severity === "low"
    ).length,
  };

  const alertSeverityCounts = {
    critical: alerts.filter(
      (alert) => alert.severity === "critical"
    ).length,

    high: alerts.filter(
      (alert) => alert.severity === "high"
    ).length,

    medium: alerts.filter(
      (alert) => alert.severity === "medium"
    ).length,

    low: alerts.filter(
      (alert) => alert.severity === "low"
    ).length,
  };

  const eventTypeCounts = {};

  events.forEach((event) => {
    eventTypeCounts[event.event_type] =
      (eventTypeCounts[event.event_type] || 0) + 1;
  });

  // ===========================================
  // AI Security Assistant
  // ===========================================

  const analyzeAlertWithAI = async (alert) => {
    setSelectedAlert(alert);
    setAiAnalysis(null);
    setAiError("");
    setAiLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/assistant/analyze-alert`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(alert),
        }
      );

      if (!response.ok) {
        throw new Error(
          `AI analysis failed: ${response.status}`
        );
      }

      const data = await response.json();

      setAiAnalysis(data);
    } catch (error) {
      console.error(
        "AI analysis error:",
        error
      );

      setAiError(
        "Unable to generate AI analysis. Please try again."
      );
    } finally {
      setAiLoading(false);
    }
  };

  // ===========================================
  // Page Descriptions
  // ===========================================

  const pageDescriptions = {
    Dashboard:
      "Monitor threats, alerts and security activity",

    Alerts:
      "Review and investigate detected security threats",

    "Security Events":
      "Review security events received by the platform",

    Analytics:
      "Analyze security activity and threat patterns",

    "AI Security Assistant":
      "Investigate security alerts using AI and retrieved security knowledge",
  };

  // ===========================================
  // Dashboard Page
  // ===========================================

  const renderDashboard = () => (
    <>
      {/* Statistics */}

      <section className="stats-grid">
        <div className="stat-card">
          <span>Total Events</span>

          <strong>
            {loading ? "..." : summary.total_events}
          </strong>
        </div>

        <div className="stat-card">
          <span>Open Alerts</span>

          <strong>
            {loading ? "..." : summary.open_alerts}
          </strong>
        </div>

        <div className="stat-card">
          <span>Critical Alerts</span>

          <strong>
            {loading ? "..." : summary.critical_alerts}
          </strong>
        </div>

        <div className="stat-card">
          <span>ML Anomalies</span>

          <strong>
            {loading ? "..." : summary.ml_anomalies}
          </strong>
        </div>
      </section>

      {/* Analytics Preview */}

      <section className="analytics-grid">
        <div className="panel analytics-panel">
          <div className="panel-header">
            <div>
              <h3>Events by Severity</h3>

              <p>
                Distribution by security events
              </p>
            </div>
          </div>

          <div className="analytics-content">
            {Object.entries(
              eventSeverityCounts
            ).map(([severity, count]) => (
              <div
                className="analytics-item"
                key={severity}
              >
                <span className="analytics-label">
                  {severity}
                </span>

                <strong>{count}</strong>
              </div>
            ))}
          </div>
        </div>

        <div className="panel analytics-panel">
          <div className="panel-header">
            <div>
              <h3>Alerts by Severity</h3>

              <p>
                Distribution by detected alerts
              </p>
            </div>
          </div>

          <div className="analytics-content">
            {Object.entries(
              alertSeverityCounts
            ).map(([severity, count]) => (
              <div
                className="analytics-item"
                key={severity}
              >
                <span className="analytics-label">
                  {severity}
                </span>

                <strong>{count}</strong>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Event Type Distribution */}

      <section className="panel">
        <div className="panel-header">
          <div>
            <h3>Event Type Distribution</h3>

            <p>
              Breakdown of security activity by event
              type
            </p>
          </div>
        </div>

        <div className="event-type-list">
          {Object.entries(eventTypeCounts).length ===
          0 ? (
            <div className="empty-state">
              <p>No event data available.</p>
            </div>
          ) : (
            Object.entries(eventTypeCounts).map(
              ([type, count]) => (
                <div
                  className="event-type-row"
                  key={type}
                >
                  <span>
                    {type.replaceAll("_", " ")}
                  </span>

                  <strong>{count}</strong>
                </div>
              )
            )
          )}
        </div>
      </section>

      {/* Recent Alerts */}

      {renderAlerts(true)}

      {/* Recent Events */}

      {renderEvents(true)}
    </>
  );

  // ===========================================
  // Alerts Page
  // ===========================================

  const renderAlerts = (preview = false) => (
    <section className="panel">
      <div className="panel-header">
        <div>
          <h3>
            {preview
              ? "Recent Alerts"
              : "Security Alerts"}
          </h3>

          <p>
            {preview
              ? "Latest detected security threats"
              : "Review and investigate detected threats"}
          </p>
        </div>

        {!preview && (
          <span className="panel-count">
            {filteredAlerts.length} alerts
          </span>
        )}
      </div>

      {/* Alert Filter */}

      <div className="filter-bar">
        <label htmlFor="alert-severity">
          Severity
        </label>

        <select
          id="alert-severity"
          value={alertSeverity}
          onChange={(e) =>
            setAlertSeverity(e.target.value)
          }
        >
          <option value="all">
            All Severities
          </option>

          <option value="critical">
            Critical
          </option>

          <option value="high">High</option>

          <option value="medium">
            Medium
          </option>

          <option value="low">Low</option>
        </select>
      </div>

      {/* Alert List */}

      <div className="alert-list">
        {loading ? (
          <div className="empty-state">
            <p>Loading alerts...</p>
          </div>
        ) : filteredAlerts.length === 0 ? (
          <div className="empty-state">
            <h3>No alerts</h3>

            <p>
              Detected security alerts will appear
              here
            </p>
          </div>
        ) : (
          filteredAlerts
            .slice(0, preview ? 5 : undefined)
            .map((alert) => (
              <div
                className="alert-row"
                key={alert.alert_id}
                onClick={() =>
                  analyzeAlertWithAI(alert)
                }
                style={{ cursor: "pointer" }}
                title="Click to analyze with AI"
              >
                <div>
                  <strong>
                    {alert.reason}
                  </strong>

                  <p>
                    {alert.evidence?.[0]}
                  </p>
                </div>

                <span
                  className={`severity ${alert.severity}`}
                >
                  {alert.severity.toUpperCase()}
                </span>
              </div>
            ))
        )}
      </div>

      {preview && filteredAlerts.length > 5 && (
        <div className="panel-footer">
          <button
            className="view-button"
            onClick={() =>
              setActivePage("Alerts")
            }
          >
            View All Alerts
          </button>
        </div>
      )}
    </section>
  );

  // ===========================================
  // Security Events Page
  // ===========================================

  const renderEvents = (preview = false) => (
    <section className="panel">
      <div className="panel-header">
        <div>
          <h3>
            {preview
              ? "Recent Security Events"
              : "Security Events"}
          </h3>

          <p>
            {preview
              ? "Latest events received by the platform"
              : "Review security events received by the platform"}
          </p>
        </div>

        {!preview && (
          <span className="panel-count">
            {filteredEvents.length} events
          </span>
        )}
      </div>

      {/* Event Filters */}

      <div className="filter-bar">
        <div className="filter-group">
          <label htmlFor="event-security">
            Severity
          </label>

          <select
            id="event-security"
            value={eventSeverity}
            onChange={(e) =>
              setEventSeverity(e.target.value)
            }
          >
            <option value="all">
              All Severities
            </option>

            <option value="critical">
              Critical
            </option>

            <option value="high">High</option>

            <option value="medium">
              Medium
            </option>

            <option value="low">Low</option>
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="event-type">
            Event Type
          </label>

          <select
            id="event-type"
            value={eventType}
            onChange={(e) =>
              setEventType(e.target.value)
            }
          >
            <option value="all">
              All Event Types
            </option>

            <option value="authentication_failure">
              Authentication Failure
            </option>

            <option value="authentication_success">
              Authentication Success
            </option>

            <option value="user_login">
              User Login
            </option>

            <option value="privilege_escalation">
              Privilege Escalation
            </option>

            <option value="unknown">
              Unknown
            </option>
          </select>
        </div>
      </div>

      {/* Event List */}

      <div className="event-list">
        {loading ? (
          <div className="empty-state">
            <p>Loading events...</p>
          </div>
        ) : filteredEvents.length === 0 ? (
          <div className="empty-state">
            <h3>No events yet</h3>

            <p>
              Incoming security events will appear
              here.
            </p>
          </div>
        ) : (
          filteredEvents
            .slice(0, preview ? 5 : undefined)
            .map((event, index) => (
              <div
                className="event-row"
                key={`${event.timestamp}-${index}`}
              >
                <div className="event-main">
                  <strong>
                    {event.event_type.replaceAll(
                      "_",
                      " "
                    )}
                  </strong>

                  <p>
                    {event.username ||
                      "Unknown user"}{" "}
                    •{" "}
                    {event.source_ip ||
                      "Unknown IP"}
                  </p>
                </div>

                <div className="event-meta">
                  <span
                    className={`severity ${event.severity}`}
                  >
                    {event.severity.toUpperCase()}
                  </span>

                  <span className="event-service">
                    {event.service ||
                      "Unknown service"}
                  </span>
                </div>
              </div>
            ))
        )}
      </div>

      {preview && filteredEvents.length > 5 && (
        <div className="panel-footer">
          <button
            className="view-button"
            onClick={() =>
              setActivePage("Security Events")
            }
          >
            View All Events
          </button>
        </div>
      )}
    </section>
  );

  // ===========================================
  // Analytics Page
  // ===========================================

  const renderAnalytics = () => (
    <>
      <section className="analytics-grid">
        <div className="panel analytics-panel">
          <div className="panel-header">
            <div>
              <h3>Events by Severity</h3>

              <p>
                Distribution of security events
              </p>
            </div>
          </div>

          <div className="analytics-content">
            {Object.entries(
              eventSeverityCounts
            ).map(([severity, count]) => (
              <div
                className="analytics-item"
                key={severity}
              >
                <span className="analytics-label">
                  {severity}
                </span>

                <strong>{count}</strong>
              </div>
            ))}
          </div>
        </div>

        <div className="panel analytics-panel">
          <div className="panel-header">
            <div>
              <h3>Alerts by Severity</h3>

              <p>
                Distribution of detected alerts
              </p>
            </div>
          </div>

          <div className="analytics-content">
            {Object.entries(
              alertSeverityCounts
            ).map(([severity, count]) => (
              <div
                className="analytics-item"
                key={severity}
              >
                <span className="analytics-label">
                  {severity}
                </span>

                <strong>{count}</strong>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <h3>Event Type Distribution</h3>

            <p>
              Breakdown of security activity by event
              type
            </p>
          </div>
        </div>

        <div className="event-type-list">
          {Object.entries(eventTypeCounts).length ===
          0 ? (
            <div className="empty-state">
              <p>No event data available.</p>
            </div>
          ) : (
            Object.entries(eventTypeCounts).map(
              ([type, count]) => (
                <div
                  className="event-type-row"
                  key={type}
                >
                  <span>
                    {type.replaceAll("_", " ")}
                  </span>

                  <strong>{count}</strong>
                </div>
              )
            )
          )}
        </div>
      </section>
    </>
  );

  // ===========================================
  // AI Security Assistant Page
  // ===========================================

  const renderAIAssistant = () => (
    <section className="panel">
      <div className="panel-header">
        <div>
          <h3>AI Security Assistant</h3>

          <p>
            Analyze security alerts using RAG and
            Google Gemini
          </p>
        </div>
      </div>

      {alerts.length === 0 ? (
        <div className="empty-state">
          <h3>No alerts available</h3>

          <p>
            Security alerts will appear here for AI
            analysis.
          </p>
        </div>
      ) : (
        <div className="ai-assistant-content">

          {/* Alert Selection */}

          <div className="ai-alert-selector">
            <h4>Select an alert to analyze</h4>

            <div className="alert-list">
              {alerts.map((alert) => (
                <div
                  className={`alert-row ${
                    selectedAlert?.alert_id ===
                    alert.alert_id
                      ? "selected-alert"
                      : ""
                  }`}
                  key={alert.alert_id}
                  onClick={() =>
                    analyzeAlertWithAI(alert)
                  }
                  style={{ cursor: "pointer" }}
                >
                  <div>
                    <strong>
                      {alert.reason}
                    </strong>

                    <p>
                      {alert.evidence?.[0]}
                    </p>
                  </div>

                  <span
                    className={`severity ${alert.severity}`}
                  >
                    {alert.severity.toUpperCase()}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* AI Result */}

          <div className="ai-analysis-panel">
            <h4>AI Analysis</h4>

            {!selectedAlert && (
              <div className="empty-state">
                <p>
                  Select an alert to start AI
                  analysis.
                </p>
              </div>
            )}

            {aiLoading && (
              <div className="empty-state">
                <p>
                  AI analyst is analyzing the
                  alert...
                </p>
              </div>
            )}

            {aiError && (
              <div className="empty-state">
                <p>{aiError}</p>
              </div>
            )}

            {aiAnalysis && !aiLoading && (
              <div className="ai-result">

                <div className="ai-result-header">
                  <span>Alert</span>

                  <strong>
                    {aiAnalysis.alert_id}
                  </strong>
                </div>

                <div className="ai-result-header">
                  <span>Severity</span>

                  <span
                    className={`severity ${
                      aiAnalysis.severity
                    }`}
                  >
                    {aiAnalysis.severity?.toUpperCase()}
                  </span>
                </div>

                {aiAnalysis.analysis && (
                  <div className="analysis-text">
                    <h4>Security Analysis</h4>

                    <div className="analysis-content">
                      {aiAnalysis.analysis}
                    </div>
                  </div>
                )}

                {aiAnalysis.knowledge?.length > 0 && (
                  <div className="knowledge-section">
                    <h4>
                      Retrieved Security Knowledge
                    </h4>

                    {aiAnalysis.knowledge.map(
                      (item, index) => (
                        <div
                          className="knowledge-item"
                          key={`${item.source}-${index}`}
                        >
                          <strong>
                            {item.source}
                          </strong>

                          <span>
                            Relevance: {item.score}
                          </span>
                        </div>
                      )
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </section>
  );

  // ===========================================
  // Render Active Page
  // ===========================================

  const renderActivePage = () => {
    switch (activePage) {
      case "Alerts":
        return renderAlerts();

      case "Security Events":
        return renderEvents();

      case "Analytics":
        return renderAnalytics();

      case "AI Security Assistant":
        return renderAIAssistant();

      case "Dashboard":
      default:
        return renderDashboard();
    }
  };

  // ===========================================
  // Main UI
  // ===========================================

  return (
    <div className="app">

      {/* Top Header */}

      <header className="topbar">
        <div>
          <h1>
            AI Cyber Threat Detection
          </h1>

          <p>SIEM Dashboard</p>
        </div>

        <div className="system-status">
          <span className="status-dot"></span>

          System Operational
        </div>
      </header>

      <div className="dashboard">

        {/* Sidebar */}

        <aside className="sidebar">
          <div className="sidebar-title">
            Security Center
          </div>

          <nav>
            {[
              "Dashboard",
              "Alerts",
              "Security Events",
              "Analytics",
              "AI Security Assistant",
            ].map((page) => (
              <button
                key={page}
                className={`nav-item ${
                  activePage === page
                    ? "active"
                    : ""
                }`}
                onClick={() =>
                  setActivePage(page)
                }
              >
                {page}
              </button>
            ))}
          </nav>
        </aside>

        {/* Main Content */}

        <main className="content">

          {/* Page Heading */}

          <section className="page-heading">
            <div>
              <h2>{activePage}</h2>

              <p>
                {pageDescriptions[activePage]}
              </p>
            </div>
          </section>

          {/* Active Page */}

          {renderActivePage()}

        </main>
      </div>
    </div>
  );
}

export default App;