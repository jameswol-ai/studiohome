"""Parametric 2D architectural floor-plan and documentation studio."""
from __future__ import annotations
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ELEMENTS={"Walls":"walls","Doors":"doors","Windows":"windows","Furniture":"furniture","Toilets":"toilets","Kitchens":"kitchens","Stairs":"stairs","Lifts":"lifts","Columns":"columns","Structural grid":"grid","Dimensions":"dimensions","Annotations":"annotations","MEP fixtures":"mep"}
VIEWS=["Ground Floor Plan","Typical Floor Plan","Roof Plan","Reflected Ceiling Plan","Furniture Plan","Fire & Life Safety Plan","HVAC Coordination Plan","Electrical Plan","Plumbing Plan","Section A-A","Section B-B","North Elevation","South Elevation","East Elevation","West Elevation","Wall Detail","Door Detail","Window Detail","Stair Detail","Toilet Detail"]
BLACK="#000000"; RED="#D40000"

def _dims():
    p=st.session_state.project
    return max(float(p.get("floorplate_width",32)),8),max(float(p.get("floorplate_depth",24)),8)

def _line(fig,x0,y0,x1,y1,width=2,dash=None):
    line=dict(color=BLACK,width=width)
    if dash: line["dash"]=dash
    fig.add_shape(type="line",x0=x0,y0=y0,x1=x1,y1=y1,line=line)

def _rect(fig,x0,y0,x1,y1,width=2,fill="rgba(0,0,0,0)"):
    fig.add_shape(type="rect",x0=x0,y0=y0,x1=x1,y1=y1,line=dict(color=BLACK,width=width),fillcolor=fill)

def _label(fig,x,y,text,size=10):
    fig.add_annotation(x=x,y=y,text=text,showarrow=False,font=dict(color=BLACK,size=size,family="Arial"))

def _plan(width,depth,visible,title):
    fig=go.Figure(); spacing=max(float(st.session_state.project.get("grid_spacing",8)),1)
    fig.update_layout(title=dict(text=title,font=dict(color=BLACK,size=20)),paper_bgcolor=RED,plot_bgcolor=RED,font=dict(color=BLACK),height=700,margin=dict(l=55,r=35,t=65,b=55),showlegend=False)
    fig.update_xaxes(range=[-4,width+4],title="metres",color=BLACK,gridcolor=BLACK,zeroline=False)
    fig.update_yaxes(range=[-4,depth+5],title="metres",color=BLACK,gridcolor=BLACK,zeroline=False,scaleanchor="x",scaleratio=1)
    if "grid" in visible:
        for x in [i*spacing for i in range(int(width/spacing)+1)]: _line(fig,x,0,x,depth,1,"dot")
        for y in [i*spacing for i in range(int(depth/spacing)+1)]: _line(fig,0,y,width,y,1,"dot")
        for i,x in enumerate([i*spacing for i in range(int(width/spacing)+1)]): _label(fig,x,depth+2,chr(65+i),9)
        for i,y in enumerate([i*spacing for i in range(int(depth/spacing)+1)]): _label(fig,-2,y,str(i+1),9)
    core_x=width*.58; core_y=depth*.52
    if "walls" in visible:
        _rect(fig,0,0,width,depth,6); _line(fig,core_x,0,core_x,depth,3); _line(fig,0,core_y,core_x,core_y,3); _rect(fig,core_x+1,depth*.60,width-1,depth*.86,3)
        _label(fig,width*.28,depth*.28,"OPEN OFFICE",13); _label(fig,width*.77,depth*.44,"CORE",12); _label(fig,width*.77,depth*.72,"SERVICE",10)
    if "doors" in visible:
        for x,y,dx,dy in [(core_x,depth*.20,2,0),(core_x,depth*.68,2,0),(width*.30,core_y,0,2)]: _line(fig,x,y,x+dx,y+dy,5)
    if "windows" in visible:
        for x in [width*.12,width*.28,width*.72,width*.86]: _line(fig,x,0,min(x+2,width),0,7); _line(fig,x,depth,min(x+2,width),depth,7)
        for y in [depth*.18,depth*.38,depth*.64,depth*.82]: _line(fig,0,y,0,min(y+1.5,depth),7); _line(fig,width,y,width,min(y+1.5,depth),7)
    if "columns" in visible:
        for x in [i*spacing for i in range(1,int(width/spacing))]:
            for y in [i*spacing for i in range(1,int(depth/spacing))]: fig.add_trace(go.Scatter(x=[x],y=[y],mode="markers",marker=dict(size=10,symbol="square",color=BLACK),showlegend=False))
    if "furniture" in visible:
        for x,y,w,h in [(3,3,5,2),(12,3,5,2),(3,depth*.62,5,2),(12,depth*.62,5,2),(width*.68,3,6,3)]:
            if x<width and y<depth: _rect(fig,x,y,min(x+w,width-1),min(y+h,depth-1),2)
    if "toilets" in visible:
        for x in [width*.68,width*.77,width*.86]: fig.add_trace(go.Scatter(x=[x],y=[depth*.73],mode="markers",marker=dict(size=14,symbol="circle-open",color=BLACK),showlegend=False))
    if "kitchens" in visible: _rect(fig,width*.62,depth*.58,width*.92,depth*.67,2); _label(fig,width*.77,depth*.625,"KITCHEN",9)
    if "stairs" in visible:
        for i in range(9): _line(fig,width*.39,depth*.08+i*.45,width*.52,depth*.08+i*.45,1)
        _label(fig,width*.455,depth*.08+4*.45,"STAIR",9)
    if "lifts" in visible: _rect(fig,width*.78,depth*.35,width*.90,depth*.49,3); _label(fig,width*.84,depth*.42,"LIFT",9)
    if "mep" in visible:
        for x,y in [(width*.64,depth*.23),(width*.74,depth*.23),(width*.84,depth*.23),(width*.64,depth*.52),(width*.74,depth*.52)]: fig.add_trace(go.Scatter(x=[x],y=[y],mode="markers",marker=dict(size=8,symbol="diamond",color=BLACK),showlegend=False))
    if "dimensions" in visible:
        _line(fig,0,-2,width,-2,1); _label(fig,width/2,-2,f"{width:.1f} m",10); _line(fig,-2,0,-2,depth,1); _label(fig,-2,depth/2,f"{depth:.1f} m",10)
    if "annotations" in visible: _label(fig,width-2,depth+3,"N",16); _line(fig,width-2,depth+1,width-2,depth+3,2)
    return fig

def _elevation(width,height,title):
    fig=go.Figure(); _rect(fig,0,0,width,height,5); levels=max(int(st.session_state.project.get("floors",12)),1)
    for i in range(1,levels): _line(fig,0,i*height/levels,width,i*height/levels,1)
    for level in range(levels):
        y0=level*height/levels+.7; y1=min(y0+height/levels*.45,height-.2)
        for x in [2,6,10,14,18,22,26,30]:
            if x<width: _rect(fig,x,y0,min(x+2.5,width-.5),y1,1)
    fig.update_layout(title=title,paper_bgcolor=RED,plot_bgcolor=RED,font=dict(color=BLACK),height=650,showlegend=False); fig.update_xaxes(color=BLACK,title="metres"); fig.update_yaxes(color=BLACK,title="metres"); return fig

def _detail(kind):
    fig=go.Figure()
    if kind=="Door Detail": _rect(fig,0,0,1,2.1,5); _line(fig,0,0,1,0,3)
    elif kind=="Window Detail": _rect(fig,0,0,2,1.5,5); _line(fig,1,0,1,1.5,2)
    elif kind=="Stair Detail":
        for i in range(8): _line(fig,i*.35,i*.22,(i+1)*.35,i*.22,3)
    elif kind=="Toilet Detail": _rect(fig,-1.2,-1,1.2,1,3)
    else: _rect(fig,0,0,3,2,5); _line(fig,0,.5,3,.5,2)
    fig.update_layout(title=kind,paper_bgcolor=RED,plot_bgcolor=RED,font=dict(color=BLACK),height=600,showlegend=False); fig.update_xaxes(scaleanchor="y",scaleratio=1,color=BLACK); fig.update_yaxes(color=BLACK); return fig

def render():
    st.markdown("## Drawing Studio | 2D Plans, Sections, Elevations and Details")
    st.caption("Parametric architectural documentation workspace with floor-plan graphics, structural grids, dimensions and coordinated building elements.")
    project=st.session_state.project; width,depth=_dims(); height=float(project.get("floor_to_floor",3.5))*int(project.get("floors",12))
    with st.container(border=True):
        c1,c2,c3,c4=st.columns(4); width=c1.number_input("Floorplate width (m)",8.0,200.0,width,1.0,key="draw_width"); depth=c2.number_input("Floorplate depth (m)",8.0,200.0,depth,1.0,key="draw_depth"); mode=c3.selectbox("View mode",["2D Documentation","3D Model","Presentation"]); view=c4.selectbox("Drawing view",VIEWS); project["floorplate_width"]=width; project["floorplate_depth"]=depth
    if mode=="2D Documentation":
        if view in ("Section A-A","Section B-B") or "Elevation" in view: fig=_elevation(width,height,view)
        elif "Detail" in view: fig=_detail(view)
        else:
            selected=st.multiselect("Visible drawing layers",list(ELEMENTS.keys()),default=list(ELEMENTS.keys()),key="drawing_layers"); fig=_plan(width,depth,{ELEMENTS[e] for e in selected},view)
        st.plotly_chart(fig,use_container_width=True)
    elif mode=="3D Model":
        fig=go.Figure(); floors=int(project.get("floors",12)); f2f=float(project.get("floor_to_floor",3.5)); faces=[(0,1,2),(0,2,3),(4,6,5),(4,7,6),(0,4,5),(0,5,1),(1,5,6),(1,6,2),(2,6,7),(2,7,3),(3,7,4),(3,4,0)]; i,j,k=zip(*faces)
        for level in range(floors):
            z=level*f2f; x=[0,width,width,0,0,width,width,0]; y=[0,0,depth,depth,0,0,depth,depth]; zz=[z,z,z,z,z+f2f,z+f2f,z+f2f,z+f2f]; fig.add_trace(go.Mesh3d(x=x,y=y,z=zz,i=i,j=j,k=k,opacity=.16,color=BLACK,name=f"Level {level+1}",showlegend=False))
        fig.update_layout(title=f"3D Building Mass | {floors} Levels",paper_bgcolor=RED,plot_bgcolor=RED,font=dict(color=BLACK),height=700,scene=dict(aspectmode="data")); st.plotly_chart(fig,use_container_width=True)
    else: st.plotly_chart(_plan(width,depth,set(ELEMENTS.values()),"Presentation Floor Plan"),use_container_width=True)
    schedule=pd.DataFrame([["Walls","A-WALL","External / partition","Coordinated"],["Doors","A-DOOR","Single / double / fire","Coordinated"],["Windows","A-WIND","Glazing / opening","Coordinated"],["Columns","S-COL","Structural grid","Structural"]],columns=["Element","Tag","Description","Status"])
    st.markdown("### Drawing Element Schedule"); st.dataframe(schedule,use_container_width=True,hide_index=True); st.download_button("Export Drawing Schedule CSV",schedule.to_csv(index=False).encode("utf-8"),"drawing_schedule.csv","text/csv")
