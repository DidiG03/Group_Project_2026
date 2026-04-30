from django import forms


def apply_bootstrap_classes(form):
    for field in form.fields.values():
        widget = field.widget
        existing = widget.attrs.get("class", "")
        if isinstance(widget, (forms.CheckboxInput,)):
            css = "form-check-input"
        elif isinstance(widget, (forms.CheckboxSelectMultiple,)):
            css = "form-check-input"
        elif isinstance(widget, (forms.SelectMultiple,)):
            css = "form-select"
        elif isinstance(widget, forms.Select):
            css = "form-select"
        else:
            css = "form-control"
        widget.attrs["class"] = (existing + " " + css).strip()
