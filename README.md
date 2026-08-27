# Streamlit Workspace Portal

Public launcher for the Streamlit apps owned by `wayneyang0204`.

Live portal: <https://shieldcoating-workspace.streamlit.app/>

The card registry is stored in `portal_apps.json`. New apps can be added by
updating that file; Streamlit Community Cloud redeploys the portal after the
change reaches `main`.

The existing Codex Streamlit maintenance heartbeat checks the owner's
Streamlit dashboard every eight hours. When it finds a new deployed app, it
adds a card to the registry and pushes the update. The portal app itself is
excluded to avoid a self-link, and existing entries are not deleted
automatically.

The repository intentionally contains no application secrets, customer data,
or private business logic.
