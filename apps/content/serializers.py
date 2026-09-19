from rest_framework import serializers

from .models import Equipment, Feature, Partner, SiteSettings, Statistic, TeamMember


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = (
            'logo',
            'phone', 'email', 'address', 'working_hours', 'map_url',
            'instagram_url', 'telegram_url', 'facebook_url', 'youtube_url',
            'hero_image', 'hero_video_url',
        )


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = ('id', 'value', 'suffix', 'label')


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ('id', 'title', 'description', 'icon', 'theme')


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ('id', 'title', 'description', 'icon', 'theme', 'image')


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ('id', 'name', 'role', 'photo', 'bio', 'telegram_url', 'linkedin_url')


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ('id', 'name', 'logo', 'url')
