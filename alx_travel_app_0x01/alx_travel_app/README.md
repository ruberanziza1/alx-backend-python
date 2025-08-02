# ALX Travel App - Milestone: Models, Serializers, and Seeder

This milestone implements:

- ✅ **Listing, Booking, and Review models** with appropriate relationships and fields.
- ✅ **Serializers** for Listing and Booking to support API endpoints.
- ✅ **Custom seeder command** to populate the database with sample listings.

### 🔍 Models Overview

- **Listing**: title, description, location, price_per_night, available, created_at
- **Booking**: ForeignKey to Listing, user info, check-in/out
- **Review**: ForeignKey to Listing, user name, rating, comment

### 📦 Seeder Command

To populate database with demo listings:
```bash
python manage.py seed
