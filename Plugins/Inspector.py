from Datamatic.Plugin import Plugin, compmethod, attrmethod
from Datamatic import Types

class Inspector(Plugin):

    @compmethod
    def GuizmoSettings(comp, flags):
        if comp["Name"] == "TransformComponent":
            return "ImGuiXtra::GuizmoSettings(mode, coords);"
        return ""
    
    @compmethod
    def Guizmo(comp, flags):
        if comp["Name"] == "TransformComponent":
            return "ShowGuizmo(editor, c, mode, coords);"
        return ""

    @attrmethod
    def Display(attr, flags):
        name = attr["Name"]
        display = attr["DisplayName"]
        cpp_type = attr["Type"]
        cpp_subtype = attr.get("Data", {}).get("Subtype")
        limits = attr.get("Data", {}).get("Limits")

        if cpp_type == "std::string":
            if cpp_subtype == "File":
                filt = attr["Data"]
                return f'ImGuiXtra::File("{display}", editor.GetWindow(), &c.{name}, "{filt}")'
            return f'ImGuiXtra::TextModifiable(c.{name})'
        if cpp_type == "float":
            if limits is not None:
                a, b = [Types.Float(x) for x in limits]
                return f'ImGui::SliderFloat("{display}", &c.{name}, {a}, {b})'
            return f'ImGui::DragFloat("{display}", &c.{name}, 0.1f)'
        if cpp_type == "Maths::vec2":
            return f'ImGui::DragFloat2("{display}", &c.{name}.x, 0.1f)'
        if cpp_type == "Maths::vec3":
            if cpp_subtype == "Colour":
                return f'ImGui::ColorPicker3("{display}", &c.{name}.r)'
            return f'ImGui::DragFloat3("{display}", &c.{name}.x, 0.1f)'
        if cpp_type == "Maths::vec4":
            if cpp_subtype == "Colour":
                return f'ImGui::ColorPicker4("{display}", &c.{name}.r)'
            return f'ImGui::DragFloat4("{display}", &c.{name}.x, 0.1f)'
        if cpp_type == "Maths::quat":
            return f'ImGuiXtra::Euler("{display}", &c.{name})'
        if cpp_type == "bool":
            return f'ImGui::Checkbox("{display}", &c.{name})'
        
        # Things like vectors and matrices and queues will get ignored for now
        return ""