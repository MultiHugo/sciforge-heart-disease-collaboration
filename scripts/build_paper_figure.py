"""Build matching SVG and native, editable Draw.io scientific figures.

The common scene uses only text, rectangles, ellipses and polylines. Icons are
editable vector primitives; no embedded bitmap or external font is required.
"""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper/case-02-heart-disease/figures"
W, H = 1200, 950
INK, MUTED, BLUE, TEAL, AMBER = "#182D40", "#526576", "#286390", "#25796F", "#946123"
RULE, PALE, WHITE = "#D4DFE6", "#F3F7FA", "#FFFFFF"
svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg", width=str(W), height=str(H), viewBox=f"0 0 {W} {H}", role="img")
ET.SubElement(svg, "title").text = "Heart Disease: cross-review and the supplementary VA audit"
ET.SubElement(svg, "desc").text = "Three local analyses lead to a review of VA accuracy and AUROC. A later audit finds 34 correct predictions, versus 35 for the all-positive baseline, among 45 test cases."
mx = ET.Element("mxfile", host="app.diagrams.net", type="device")
diagram = ET.SubElement(mx, "diagram", id="heart-case", name="Heart Disease case")
graph = ET.SubElement(diagram, "mxGraphModel", dx=str(W), dy=str(H), grid="1", gridSize="10", page="1", pageScale="1", pageWidth=str(W), pageHeight=str(H), math="0", shadow="0")
root = ET.SubElement(graph, "root")
ET.SubElement(root, "mxCell", id="0")
ET.SubElement(root, "mxCell", id="1", parent="0")
count = 1


def cell(value, style, x, y, w, h):
    global count
    count += 1
    node = ET.SubElement(root, "mxCell", id=str(count), value=value, style=style, vertex="1", parent="1")
    ET.SubElement(node, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h), **{"as": "geometry"})
    return node


def box(x, y, w, h, fill=WHITE, stroke=RULE, radius=8, sw=1.4):
    ET.SubElement(svg, "rect", x=str(x), y=str(y), width=str(w), height=str(h), rx=str(radius), fill=fill, stroke=stroke, **{"stroke-width": str(sw)})
    cell("", f"rounded={int(radius > 0)};arcSize=8;whiteSpace=wrap;html=0;fillColor={fill};strokeColor={stroke};strokeWidth={sw};", x, y, w, h)


def oval(x, y, w, h, fill="none", stroke=BLUE, sw=2):
    ET.SubElement(svg, "ellipse", cx=str(x+w/2), cy=str(y+h/2), rx=str(w/2), ry=str(h/2), fill=fill, stroke=stroke, **{"stroke-width": str(sw)})
    cell("", f"ellipse;fillColor={fill};strokeColor={stroke};strokeWidth={sw};", x, y, w, h)


def line(points, color=RULE, sw=1.8, arrow=False, dashed=False):
    global count
    ET.SubElement(svg, "polyline", points=" ".join(f"{x},{y}" for x,y in points), fill="none", stroke=color, **{"stroke-width": str(sw), "stroke-linecap": "round", "stroke-linejoin": "round", "stroke-dasharray": "6 5" if dashed else "none"})
    if arrow:
        x,y = points[-1]
        px,py = points[-2]
        import math
        angle = math.atan2(y-py, x-px)
        pts = [(x-8*math.cos(angle-.45), y-8*math.sin(angle-.45)), (x,y), (x-8*math.cos(angle+.45), y-8*math.sin(angle+.45))]
        ET.SubElement(svg, "polyline", points=" ".join(f"{a},{b}" for a,b in pts), fill="none", stroke=color, **{"stroke-width": str(sw), "stroke-linecap": "round", "stroke-linejoin": "round"})
    count += 1
    node = ET.SubElement(root, "mxCell", id=str(count), style=f"edgeStyle=none;rounded=0;endArrow={'open' if arrow else 'none'};endFill=0;endSize=8;strokeColor={color};strokeWidth={sw};dashed={int(dashed)};", edge="1", parent="1")
    geom = ET.SubElement(node, "mxGeometry", relative="1", **{"as": "geometry"})
    ET.SubElement(geom, "mxPoint", x=str(points[0][0]), y=str(points[0][1]), **{"as": "sourcePoint"})
    ET.SubElement(geom, "mxPoint", x=str(points[-1][0]), y=str(points[-1][1]), **{"as": "targetPoint"})
    if len(points) > 2:
        arr = ET.SubElement(geom, "Array", **{"as": "points"})
        for x,y in points[1:-1]:
            ET.SubElement(arr, "mxPoint", x=str(x), y=str(y))


def text(x, y, value, size=22, color=INK, bold=False, width=500, align="left"):
    tx = x if align == "left" else x+width/2 if align == "center" else x+width
    anchor = {"left":"start", "center":"middle", "right":"end"}[align]
    node = ET.SubElement(svg, "text", x=str(tx), y=str(y+size*.84), fill=color, **{"text-anchor":anchor, "style":f"font:{'700 ' if bold else ''}{size}px Arial, Helvetica, sans-serif"})
    node.text = value
    cell(value, f"text;html=0;whiteSpace=nowrap;overflow=visible;align={align};verticalAlign=top;spacing=0;fontFamily=Arial;fontSize={size};fontStyle={int(bold)};fontColor={color};strokeColor=none;fillColor=none;", x, y, width, size*1.25)


def icon(name, x, y, color=BLUE):
    """32px stroke icons, built from the same primitives in both exports."""
    def p(points):
        line([(x+a,y+b) for a,b in points], color, 2)
    if name == "database":
        oval(x+3,y+3,26,8,WHITE,color)
        p([(3,7),(3,25)])
        p([(29,7),(29,25)])
        oval(x+3,y+21,26,8,WHITE,color)
        p([(3,14),(8,17),(16,18),(24,17),(29,14)])
    elif name in ("report", "check"):
        p([(5,2),(21,2),(28,9),(28,30),(5,30),(5,2)])
        p([(21,2),(21,9),(28,9)])
        if name == "report":
            p([(10,15),(23,15)])
            p([(10,21),(23,21)])
            p([(10,26),(18,26)])
        else:
            p([(10,21),(15,26),(24,15)])
    elif name == "review":
        oval(x+2,y+2,21,21,"none",color)
        p([(21,21),(30,30)])
        p([(8,12),(12,16),(18,9)])
    elif name == "chart":
        p([(3,2),(3,29),(30,29)])
        p([(8,23),(14,14),(21,17),(29,6)])
    elif name == "people":
        oval(x+3,y+3,10,10,"none",color)
        oval(x+19,y+3,10,10,"none",color)
        p([(1,29),(2,21),(6,18),(10,18),(14,21),(15,29)])
        p([(17,29),(18,21),(22,18),(26,18),(30,21),(31,29)])


box(0,0,W,H,WHITE,"none",0)
text(40,24,"Heart Disease: how cross-review changed the analysis",30,bold=True,width=1120)
text(40,68,"Research question: do local models distinguish positive and negative cases?",23,MUTED,width=1120)

box(40,120,1120,95,PALE)
icon("database",62,145)
text(110,137,"1  Set up a common study",25,BLUE,True,width=1020)
text(110,176,"UCI Heart Disease · three institutional partitions · one logistic-regression workflow",23,width=1020)
line([(600,215),(600,250)],BLUE,1.8,True)
box(40,260,1120,217,"#FAFCFD")
text(60,274,"2  Run local analyses in separate workspaces",24,BLUE,True,width=1080)

for x,place,role in [(60,"Cleveland","B · analyst and coordinator"),(438,"Hungarian","C · analyst and reviewer"),(816,"VA","D · analyst")]:
    box(x,320,324,137)
    icon("people",x+16,339)
    text(x+60,337,place,25,bold=True,width=250)
    text(x+16,374,role,21,BLUE,width=294)
    text(x+16,410,"Train and evaluate a local model",20,width=294)
line([(222,457),(222,493),(978,493),(978,457)],BLUE,1.7)
line([(600,457),(600,493)],BLUE,1.7)
line([(222,493),(222,537)],BLUE,1.7,True)
text(420,505,"Share methods and aggregate results only",22,BLUE,width=740)

box(40,547,1120,202,"#FAFCFD")
text(60,561,"3  Review and revise in the SciForge project",24,BLUE,True,width=1080)
for x,title,name,col,fill,lines in [
    (60,"B combines reports","report",BLUE,PALE,["Three local baselines in","one shared research record"]),
    (438,"C questions VA accuracy","review",AMBER,"#FCF8F0",["75.56% correct, yet weak","discrimination (AUROC 0.5629)"]),
    (816,"B revises the report","check",TEAL,"#F1F7F5",["Add class balance and AUROC;","propose repeated-split checks"]),
]:
    box(x,603,324,125,fill)
    icon(name,x+14,618,col)
    text(x+55,619,title,22,col,True,width=260)
    for i,s in enumerate(lines):
        text(x+16,661+i*27,s,21,width=294)
line([(384,667),(435,667)],BLUE,1.8,True)
line([(762,667),(813,667)],BLUE,1.8,True)
line([(600,728),(600,800)],AMBER,1.8,True,True)
text(625,764,"Question for follow-up",21,AMBER,width=290)

box(40,810,1120,116,"#F1F7F5")
icon("chart",60,829,TEAL)
text(108,826,"4  Follow-up analysis: reconstruct the same 45 VA test cases",24,TEAL,True,width=1030)
text(108,863,"Model: 34/45 correct  ·  Predict all positive: 35/45 correct",23,bold=True,width=1030)
text(108,894,"Finding: the model did not outperform this simple baseline on accuracy.",21,width=1030)

OUT.mkdir(parents=True,exist_ok=True)
for name, tree in [("fig5_heart_disease.svg",svg),("fig5_heart_disease.drawio",mx)]:
    ET.indent(tree,space="  ")
    (OUT/name).write_bytes(ET.tostring(tree,encoding="utf-8",xml_declaration=True)+b"\n")
print(f"Wrote SVG and {count-1} native Draw.io objects to {OUT}")

# Optional vector PDF export. A temporary browser profile keeps this independent
# of any running interactive Chrome session.
if __name__ == "__main__":
    import argparse
    import os
    import shutil
    import subprocess
    import tempfile
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", action="store_true")
    parser.add_argument("--chrome", default=shutil.which("google-chrome") or shutil.which("chromium") or "C:/Program Files/Google/Chrome/Application/chrome.exe")
    args = parser.parse_args()
    if args.pdf:
        with tempfile.TemporaryDirectory(prefix="heart-figure-") as temp:
            temp = Path(temp)
            page = temp / "figure.html"
            page.write_text(f'<meta charset="utf-8"><style>@page{{size:{W}px {H}px;margin:0}}html,body{{margin:0;width:{W}px;height:{H}px}}svg{{display:block}}</style>'+ET.tostring(svg,encoding="unicode"), encoding="utf-8")
            command = [args.chrome,"--headless","--disable-gpu","--no-pdf-header-footer",f"--user-data-dir={temp/'profile'}",f"--print-to-pdf={OUT/'fig5_heart_disease.pdf'}",page.as_uri()]
            startupinfo = None
            if os.name == "nt":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
            result = subprocess.run(command,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=60,startupinfo=startupinfo)
            if result.returncode:
                raise RuntimeError(result.stderr)
        print("Exported vector PDF")
