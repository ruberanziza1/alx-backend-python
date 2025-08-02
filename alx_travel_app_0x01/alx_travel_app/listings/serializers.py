#from rest_framework import serializers
#from .models import Listing, Booking

#class ListingSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Listing
#        fields = '__all__'


#class BookingSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Booking
#        fields = '__all__'


from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Listing, Booking, Review, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(max_length=500)

    class Meta:
        model = Review
        fields = ['id', 'user', 'listing', 'rating', 'comment', 'created_at']


class ListingSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            "id", "name", "description", "location", "price_per_night",
            "host", "reviews", "average_rating", "created_at", "updated_at"
        ]

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return None
        return round(sum([r.rating for r in reviews]) / len(reviews), 1)


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)
    status = serializers.CharField()

    class Meta:
        model = Booking
        fields = ['id', 'listing', 'user', 'start_date', 'end_date', 'status', 'created_at']

    def validate(self, data):
        if 'start_date' in data and 'end_date' in data:
            if data['start_date'] > data['end_date']:
                raise ValidationError("End date must be after start date.")
        return data
