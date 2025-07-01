from nicegui import app, ui

# Import all pages to register their routes
from pages import routers

# Apply Element UI inspired global styles
# ui.add_css("styles/element.css")

app.include_router(routers.prod_router)

@ui.page('/')
def redirect_to_product():
    ui.navigate.to('/product/product-management')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="Production Management", 
        favicon="🏭", 
        reload=True,
        dark=False  # Force light mode to match Element UI
    )
