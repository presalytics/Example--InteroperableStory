# Section 1: Build qualitive data
# Build qualitative data from metrics to load into template widget
import presalytics
from analysis import (
    r_squared,
    beta,
)

fit_quality_lookup = (
    (.95, "wow!"),
    (.8, "pretty good"),
    (.7, "good-ish"),
    (.5, "so-so"),
    (.2, "meh"),
    (0, "bad")
)
fit_quality = next(x[1] for x in fit_quality_lookup if r_squared >= x[0])
trend = "positive" if beta > 0 else "negitive"
if trend == "negitive":
    header_color = "FF0000"  # Red Hex color
else:
    header_color = "00FF00"  # Green Hex Color

# Section 2: Dynamically building widget parameters
# Set that parameters for a `prealtyics.MultiXmlTransform` XmlTransform
params = {"transforms_list": [
    {
        'name': 'TextReplace',
        'function_params': {
            'trend': trend,
            'beta': str(round(beta, 2)),
            'r_squared': str(round(r_squared * 100, 2)) + "%",
            'fit_quality': fit_quality
        },
    },
    {
        'name': 'ChangeShapeColor',
        'function_params': {
            'hex_color': header_color,
            'object_name': "header"  # From the 'Selection Pane' of PowerPoint
        }
    }
]}
# Collect data from the Presaltyics API so the OoxmlEditorWidget can dynamically update
story_id = presalytics.StoryOutline.import_yaml("story.yaml").story_id
client = presalytics.Client()
story = client.story.story_id_get(story_id, include_relationships=True)
document_ooxml_id = story.ooxml_documents[0].ooxml_automation_id
document_tree = client.ooxml_automation.documents_childobjects_get_id(document_ooxml_id)

takeaway_box_id = next(o.entity_id for o in document_tree if o.entity_name == "TakeawayBox")

# Section 3: Creating a Widget instance
# Create an instance of `OoxmlEditorWidget` that will update each time the outline is pushed 
template_widget = presalytics.OoxmlEditorWidget(
    "Takeaways Box",
    story_id,
    takeaway_box_id,
    presalytics.OoxmlEndpointMap.group(),
    presalytics.MultiXmlTransform,
    transform_params=params
)
