"""Resolwe entity serializer."""
from resolwe.flow.models import Collection, Entity

from .collection import CollectionSerializer
from .fields import DictRelatedField


class EntitySerializer(CollectionSerializer):
    """Serializer for Entity."""

    collection = DictRelatedField(
        queryset=Collection.objects.all(),
        serializer=CollectionSerializer,
        allow_null=True,
        required=False,
        write_permission="edit",
    )

    class Meta(CollectionSerializer.Meta):
        """EntitySerializer Meta options."""

        model = Entity
        fields = CollectionSerializer.Meta.fields + (
            "collection",
            "duplicated",
            "type",
        )

    def update(self, instance, validated_data):
        """Update."""
        source_collection = instance.collection
        instance = super().update(instance, validated_data)
        instance.move_to_collection(source_collection, instance.collection)

        return instance
