from bpy.types import Panel, UIList
from blenderbim.bim.ifc import IfcStore
from ifcopenshell.api.cost.data import Data


class BIM_PT_cost_schedules(Panel):
    bl_label = "IFC Cost Schedules"
    bl_idname = "BIM_PT_cost_schedules"
    bl_options = {"DEFAULT_CLOSED"}
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"

    @classmethod
    def poll(cls, context):
        return IfcStore.get_file()

    def draw(self, context):
        props = context.scene.BIMCostProperties

        if not Data.is_loaded:
            Data.load(IfcStore.get_file())

        row = self.layout.row()
        row.operator("bim.add_cost_schedule", icon="ADD")

        for cost_schedule_id, cost_schedule in Data.cost_schedules.items():
            row = self.layout.row(align=True)
            row.label(text=cost_schedule["Name"] or "Unnamed", icon="LINENUMBERS_ON")

            if props.active_cost_schedule_id and props.active_cost_schedule_id == cost_schedule_id:
                row.operator("bim.edit_cost_schedule", text="", icon="CHECKMARK")
                row.operator("bim.disable_editing_cost_schedule", text="", icon="X")
            elif props.active_cost_schedule_id:
                row.operator("bim.remove_cost_schedule", text="", icon="X").cost_schedule = cost_schedule_id
            else:
                row.operator("bim.enable_editing_cost_schedule", text="", icon="GREASEPENCIL").cost_schedule = cost_schedule_id
                row.operator("bim.remove_cost_schedule", text="", icon="X").cost_schedule = cost_schedule_id

            if props.active_cost_schedule_id == cost_schedule_id:
                for attribute in props.cost_schedule_attributes:
                    row = self.layout.row(align=True)
                    if attribute.data_type == "string":
                        row.prop(attribute, "string_value", text=attribute.name)
                    elif attribute.data_type == "enum":
                        row.prop(attribute, "enum_value", text=attribute.name)
                    if attribute.is_optional:
                        row.prop(attribute, "is_null", icon="RADIOBUT_OFF" if attribute.is_null else "RADIOBUT_ON", text="")
