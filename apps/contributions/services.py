from .models import EntityEditHistory

TRACKED_ENTITY_FIELDS = ['name', 'description', 'metadata', 'primary_image_url']

def record_entity_edits(entity, original_data, new_data, user, reason=""):
    """
    Compares original_data dict with new_data dict and creates EntityEditHistory records.
    """
    contributions = []
    for field in TRACKED_ENTITY_FIELDS:
        if field in new_data:
            old_val = str(original_data.get(field) or '').strip()
            new_val = str(new_data.get(field) or '').strip()
            if old_val != new_val:
                contrib = EntityEditHistory.objects.create(
                    entity=entity,
                    edited_by=user,
                    field_name=field,
                    previous_value=old_val,
                    new_value=new_val,
                    reason=reason or f"Updated {field}"
                )
                contributions.append(contrib)
    return contributions

# Backward compatibility alias
record_movie_edits = record_entity_edits
