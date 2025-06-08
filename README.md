# 🚕 Uber Pricing Configuration System

A configurable pricing engine built with **Django** and **Django Admin**, allowing business teams to define and manage differential ride pricing based on distance, duration, day of the week, and waiting time.

---

## Features

- Distance-Based Pricing (DBP)
- Distance Additional Pricing (DAP) slabs
- Time Multiplier Factor (TMF) slabs based on ride duration
- Waiting Charges (WC)
- Day-of-week specific pricing
- Enable/disable configurations
- Enable/Disable multiple pricing module
- Calculate final ride price using:
  > Price = (DBP + (Dn _ DAP)) + (Tn _ TMF) + WC
- Admin interface with:
- Validation
- Audit logging (who changed what, when)
- REST API to calculate pricing for a ride
