from app.tools.products_tools import(tool_get_products,tool_search_product_by_name,tool_get_products_by_min_price,tool_get_products_by_max_price)
from app.tools.cart_tools import(tool_add_to_cart,tool_remove_from_cart,tool_view_cart,tool_checkout_cart,tool_clear_cart)
from app.tools.order_tools import (tool_get_order_status,tool_get_user_orders)
from app.tools.admin_tools import (tool_activate_user,tool_add_product,tool_deactivate_user,tool_delete_user,tool_list_products, tool_list_users, tool_remove_product, tool_update_product,tool_list_orders,tool_update_order_status)
available_tools ={
    'get_products':tool_get_products,
    'search_product_by_name':tool_search_product_by_name,
    'get_products_by_max_price':tool_get_products_by_max_price,
    'get_products_by_min_price':tool_get_products_by_min_price,
    'add_to_cart':tool_add_to_cart,
    'remove_from_cart':tool_remove_from_cart,
    'view_cart':tool_view_cart,
    'checkout_cart':tool_checkout_cart,
    'get_order_status':tool_get_order_status,
    'get_user_orders':tool_get_user_orders,
    'clear_cart':tool_clear_cart,

}
USER_SCOPED_TOOLS = {
    "add_to_cart",
    "remove_from_cart",
    "view_cart",
    "checkout_cart",
    "get_order_status",
    "get_user_orders",
    "clear_cart",
}

admin_available_tools = {
    "add_product": tool_add_product,
    "list_products": tool_list_products,
    "update_product": tool_update_product,
    "remove_product": tool_remove_product,
    "list_users": tool_list_users,
    "deactivate_user": tool_deactivate_user,
    "activate_user": tool_activate_user,
    "delete_user": tool_delete_user,
    'list_orders':tool_list_orders,
    'update_order_status':tool_update_order_status,
}
ADMIN_SCOPED_TOOLS = {
    "deactivate_user",
    "activate_user",
    "delete_user",
}

