# Capacity / Reservations

## What it is

**Reservations** and **capacity commitment** let you buy BigQuery slots (flat-rate) for predictable capacity and cost. **Reservations monitoring** shows usage and assignment of slots to projects and jobs.

## Demo doc

The BQ-Features demo runs on on-demand slots by default. Use the Administration **Capacity** or **Reservations** section to show how reservations are configured and how slot usage for the demo project would appear if it were assigned to a reservation.

## Demo material

1. **Open Capacity / Reservations**  
   In BigQuery → **Administration** → **Capacity** or **Reservations** (or the reservations UI in Cloud Console). You may need admin or billing permissions.

2. **View current setup**  
   List **Reservations** and **Capacity commitments** in your org or project. Note whether the demo project uses on-demand or is assigned to a reservation. Check **Assignments** to see which projects use which reservation.

3. **Reservations monitoring**  
   Open **Reservations monitoring** or slot usage views. Filter by the demo project. Run a few demo queries and Dataform operations, then refresh. Show slot usage (slot milliseconds or active slots over time). Explain how this would change if the project were assigned to a reservation (dedicated slots).

4. **Create a reservation (optional)**  
   If you have permissions and want to demo flat-rate: create a small **capacity commitment** (e.g. 100 slots) and a **reservation**. Assign the demo project to this reservation. Run demo queries and show that they use the reserved slots. Document the cost implication for training.

5. **Document for your team**  
   Note: on-demand vs reservation, how to assign a project to a reservation, and where to see slot usage for the demo project. No change to the demo dataset itself.

## Demo data used

- Demo project (where `bq_studio_demo` lives).  
- Jobs from demo SQL and Dataform runs (for slot usage observation).  
- Reservations and assignments (optional) for capacity demo.

## References

- [Introduction to reservations](https://cloud.google.com/bigquery/docs/reservations-intro)  
- [Monitor reservations](https://cloud.google.com/bigquery/docs/reservations-monitoring)
