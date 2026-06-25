from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_admin
from app.database import get_db
from app.models import Admin, Widget
from app.schemas import WidgetCreate, WidgetUpdate, WidgetResponse

router = APIRouter(prefix="/widgets", tags=["widgets"], dependencies=[Depends(get_current_admin)])


@router.get("/", response_model=list[WidgetResponse])
def list_widgets(db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    return db.query(Widget).filter(Widget.admin_id == admin.id).order_by(Widget.z_index).all()


@router.get("/{widget_id}", response_model=WidgetResponse)
def get_widget(widget_id: int, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    widget = db.query(Widget).filter(Widget.id == widget_id, Widget.admin_id == admin.id).first()
    if not widget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Widget not found")
    return widget


@router.post("/", response_model=WidgetResponse, status_code=status.HTTP_201_CREATED)
def create_widget(
    widget_data: WidgetCreate,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    widget = Widget(**widget_data.model_dump(), admin_id=admin.id)
    db.add(widget)
    db.commit()
    db.refresh(widget)
    return widget


@router.put("/{widget_id}", response_model=WidgetResponse)
def update_widget(
    widget_id: int,
    widget_data: WidgetUpdate,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    widget = db.query(Widget).filter(Widget.id == widget_id, Widget.admin_id == admin.id).first()
    if not widget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Widget not found")
    update_fields = widget_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(widget, field, value)
    db.commit()
    db.refresh(widget)
    return widget


@router.delete("/{widget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_widget(widget_id: int, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    widget = db.query(Widget).filter(Widget.id == widget_id, Widget.admin_id == admin.id).first()
    if not widget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Widget not found")
    db.delete(widget)
    db.commit()
