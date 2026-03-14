import os
from PIL import Image, ImageDraw, ImageFont

def create_architecture_diagram(output_path):
    width, height = 800, 1000
    # Dark mode background
    img = Image.new('RGB', (width, height), color='#0f172a')
    draw = ImageDraw.Draw(img)
    
    # Try to load a nice font, otherwise use default
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 24)
        font_item = ImageFont.truetype("arial.ttf", 18)
    except:
        font_title = ImageFont.load_default()
        font_item = ImageFont.load_default()

    layers = [
        {
            "title": "Distributed Sensor Layer",
            "items": ["Drone Alpha", "Drone Beta", "Satellite Gamma"]
        },
        {
            "title": "AI Perception Pipeline",
            "items": ["YOLOv8 Detection", "ByteTrack Tracking", "Trajectory Manager", "GeoMapper"]
        },
        {
            "title": "Intelligence Engine",
            "items": ["Threat Engine", "Kalman Predictor", "LSTM Behavior Model"]
        },
        {
            "title": "Command & Control Layer",
            "items": ["FastAPI Aggregator", "WebSocket Event Stream", "Mission Logger"]
        },
        {
            "title": "Tactical Intelligence UI",
            "items": ["Leaflet Dashboard", "Threat Alerts", "Mission Replay"]
        }
    ]

    box_width = 400
    start_y = 50
    gap_y = 60
    
    current_y = start_y
    
    for i, layer in enumerate(layers):
        # Calculate box height
        box_height = 50 + len(layer["items"]) * 30 + 20
        start_x = (width - box_width) // 2
        
        # Draw box
        draw.rounded_rectangle(
            [start_x, current_y, start_x + box_width, current_y + box_height],
            radius=15,
            fill="#1e293b",
            outline="#38bdf8",
            width=3
        )
        
        # Draw title
        draw.text((start_x + 20, current_y + 15), layer["title"], font=font_title, fill="#38bdf8")
        draw.line([start_x + 20, current_y + 45, start_x + box_width - 20, current_y + 45], fill="#334155", width=2)
        
        # Draw items
        item_y = current_y + 60
        for item in layer["items"]:
            # bullet
            draw.ellipse([start_x + 25, item_y + 7, start_x + 35, item_y + 17], fill="#f43f5e")
            draw.text((start_x + 50, item_y + 2), item, font=font_item, fill="#e2e8f0")
            item_y += 30
            
        # Draw arrow to next box if not last
        if i < len(layers) - 1:
            arrow_start_y = current_y + box_height
            arrow_end_y = arrow_start_y + gap_y
            cx = width // 2
            draw.line([cx, arrow_start_y, cx, arrow_end_y - 10], fill="#94a3b8", width=4)
            # Arrow head
            draw.polygon([
                (cx, arrow_end_y),
                (cx - 10, arrow_end_y - 15),
                (cx + 10, arrow_end_y - 15)
            ], fill="#94a3b8")
            
        current_y += box_height + gap_y

    img.save(output_path)
    print(f"Diagram saved to {output_path}")

if __name__ == "__main__":
    os.makedirs("docs", exist_ok=True)
    create_architecture_diagram("docs/architecture.png")
