import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime

st.set_page_config(
    page_title="Cloud Detective",
    page_icon="🕵️",
    layout="wide"
)

st.title("🕵️ Cloud Detective")
st.caption("AI-style DevOps Incident Investigator — Kubernetes / Logs / Infra Demo")

# -----------------------------
# Demo Data
# -----------------------------

incident_types = {
    "Pod CrashLoopBackOff": {
        "severity": "High",
        "root": "Application container is repeatedly crashing after startup.",
        "impact": "Service unavailable or unstable.",
        "fix": [
            "Check container logs using kubectl logs",
            "Verify environment variables and secrets",
            "Check recent image changes",
            "Rollback to previous stable image if needed"
        ],
        "logs": [
            "ERROR: failed to connect to database",
            "Container exited with code 1",
            "Back-off restarting failed container",
            "Readiness probe failed"
        ]
    },
    "PVC Mount Failure": {
        "severity": "Critical",
        "root": "Persistent volume could not be attached or mounted.",
        "impact": "Application cannot start because storage is unavailable.",
        "fix": [
            "Check PVC status",
            "Describe pod and volume attachment",
            "Verify storage class",
            "Check CSI driver health"
        ],
        "logs": [
            "Unable to attach or mount volumes",
            "MountVolume.MountDevice failed",
            "timed out waiting for condition",
            "pod has unbound immediate PersistentVolumeClaims"
        ]
    },
    "ImagePullBackOff": {
        "severity": "Medium",
        "root": "Kubernetes cannot pull the container image.",
        "impact": "Pod remains pending and application never starts.",
        "fix": [
            "Verify image name and tag",
            "Check image registry credentials",
            "Confirm image exists",
            "Check network access from cluster"
        ],
        "logs": [
            "Failed to pull image",
            "repository does not exist",
            "pull access denied",
            "Back-off pulling image"
        ]
    },
    "Node Resource Pressure": {
        "severity": "High",
        "root": "Node does not have enough CPU or memory to schedule pods.",
        "impact": "New workloads remain pending.",
        "fix": [
            "Check node resource usage",
            "Scale node pool",
            "Reduce pod resource requests",
            "Enable cluster autoscaler"
        ],
        "logs": [
            "0/3 nodes are available",
            "Insufficient cpu",
            "Insufficient memory",
            "FailedScheduling"
        ]
    }
}

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.header("⚙️ Investigation Input")

selected_incident = st.sidebar.selectbox(
    "Choose incident type",
    list(incident_types.keys())
)

namespace = st.sidebar.text_input("Namespace", "dataflow-studio")
app_name = st.sidebar.text_input("Application", "airflow")
cluster = st.sidebar.text_input("Cluster", "demo-cluster")

run_scan = st.sidebar.button("🔍 Run Investigation", use_container_width=True)

incident = incident_types[selected_incident]

# -----------------------------
# Main Layout
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Cluster", cluster)
col2.metric("Namespace", namespace)
col3.metric("App", app_name)
col4.metric("Severity", incident["severity"])

st.divider()

if run_scan:
    st.subheader("🧪 Investigation Running")

    progress = st.progress(0)
    status = st.empty()

    steps = [
        "Collecting Kubernetes events...",
        "Reading pod logs...",
        "Checking resource pressure...",
        "Analyzing failure pattern...",
        "Generating root cause report..."
    ]

    for i, step in enumerate(steps):
        status.info(step)
        progress.progress((i + 1) * 20)
        time.sleep(0.6)

    status.success("Investigation complete")

    st.divider()

    left, right = st.columns([1.2, 1])

    with left:
        st.subheader("📌 Root Cause Analysis")

        st.error(f"Incident Detected: {selected_incident}")

        st.write("### Root Cause")
        st.write(incident["root"])

        st.write("### User Impact")
        st.write(incident["impact"])

        confidence = random.randint(86, 97)
        st.progress(confidence / 100)
        st.caption(f"Confidence Score: {confidence}%")

        st.write("### Recommended Fix")
        for fix in incident["fix"]:
            st.checkbox(fix)

    with right:
        st.subheader("📜 Evidence Logs")

        for log in incident["logs"]:
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.code(f"[{timestamp}] {log}")

    st.divider()

    st.subheader("🕒 Incident Timeline")

    timeline = pd.DataFrame({
        "Time": ["10:31", "10:32", "10:34", "10:35", "10:37"],
        "Event": [
            "Deployment triggered",
            "Pod created",
            "Warning event detected",
            selected_incident,
            "Investigation completed"
        ],
        "Status": [
            "Normal",
            "Normal",
            "Warning",
            "Failed",
            "Analyzed"
        ]
    })

    st.dataframe(timeline, use_container_width=True)

    st.subheader("🧠 AI Summary")

    st.success(
        f"""
        Cloud Detective found that **{app_name}** in namespace **{namespace}**
        is affected by **{selected_incident}**.

        Most likely cause: **{incident['root']}**

        Suggested next action: **{incident['fix'][0]}**
        """
    )

else:
    st.info("Select an incident type from the sidebar and click **Run Investigation**.")
