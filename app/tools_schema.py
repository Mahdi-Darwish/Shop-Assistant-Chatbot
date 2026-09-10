# tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "get_products",
#             "description": "Get all available products.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {},
#                 "required": [],
#                 "additionalProperties": False,
#             },
#             "strict": True,
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "search_product_by_name",
#             "description": "Search available products by name.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "name": {
#                         "type": "string",
#                         "description": "The product name or keyword to search for."
#                     }
#                 },
#                 "required": ["name"],
#                 "additionalProperties": False,
#             },
#             "strict": True,
#         },
#     },

#     {
#         "type": "function",
#         "function": {
#             "name": "get_products_by_max_price",
#             "description": "Get products with a price less than or equal to the specified maximum price.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "max_price": {
#                         "type": "number",
#                         "description": "Maximum product price."
#                     }
#                 },
#                 "required": ["max_price"],
#                 "additionalProperties": False,
#             },
#             "strict": True,
#         },
#     },

#     {
#         "type": "function",
#         "function": {
#             "name": "get_products_by_min_price",
#             "description": "Get products with a price greater than or equal to the specified minimum price.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "min_price": {
#                         "type": "number",
#                         "description": "Minimum product price."
#                     }
#                 },
#                 "required": ["min_price"],
#                 "additionalProperties": False,
#             },
#             "strict": True,
#         },
#     },
#      {
#         "type": "function",
#         "function": {
#             "name": "add_to_cart",
#             "description": (
#                 "Add a product to the current user's active shopping cart, "
#                 "identified by product name. If the name matches more than "
#                 "one product, ask the user which one they meant."
#             ),
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "product_name": {
#                         "type": "string",
#                         "description": "Name or partial name of the product to add.",
#                     },
#                     "quantity": {
#                         "type": "integer",
#                         "description": "How many units to add. Defaults to 1.",
#                     },
#                 },
#                 "required": ["product_name"],
#             },
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "remove_from_cart",
#             "description": (
#                 "Remove a product from the current user's active cart. If "
#                 "quantity is omitted, removes the product entirely; "
#                 "otherwise decreases the quantity by that amount."
#             ),
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "product_name": {
#                         "type": "string",
#                         "description": "Name or partial name of the product to remove.",
#                     },
#                     "quantity": {
#                         "type": "integer",
#                         "description": "How many units to remove. Omit to remove entirely.",
#                     },
#                 },
#                 "required": ["product_name"],
#             },
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "view_cart",
#             "description": "Show the items currently in the current user's active cart, with prices and total.",
#             "parameters": {"type": "object", "properties": {}},
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "checkout_cart",
#             "description": "Place an order from everything currently in the current user's active cart.",
#             "parameters": {"type": "object", "properties": {}},
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "get_order_status",
#             "description": "Look up the status and total of one of the current user's past orders by order id.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "order_id": {
#                         "type": "integer",
#                         "description": "The id of the order to check.",
#                     },
#                 },
#                 "required": ["order_id"],
#             },
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "get_user_orders",
#             "description": "List all past orders placed by the current user.",
#             "parameters": {"type": "object", "properties": {}},
#         },
#     },
#     {
#     "type": "function",
#     "function": {
#         "name": "clear_cart",
#         "description": "Remove everything from the current user's active cart at once, without checking out.",
#         "parameters": {"type": "object", "properties": {}},
#     },
# },

# ]
# admin_tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "add_product",
#             "description": "Add a new product to the shop's menu/catalog.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "name": {"type": "string", "description": "The product's name."},
#                     "description": {"type": "string", "description": "A short description of the product."},
#                     "price": {"type": "number", "description": "The price, e.g. 4.50."},
#                 },
#                 "required": ["name", "description", "price"],
#             },
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "list_products",
#             "description": "List every product currently in the shop's catalog.",
#             "parameters": {"type": "object", "properties": {}},
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "update_product",
#             "description": "Update an existing product's name, description, and/or price. Only the fields provided are changed.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "product_name": {"type": "string", "description": "Name of the product to update."},
#                     "new_name": {"type": "string", "description": "New name, if changing it."},
#                     "new_description": {"type": "string", "description": "New description, if changing it."},
#                     "new_price": {"type": "number", "description": "New price, if changing it."},
#                 },
#                 "required": ["product_name"],
#             },
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "remove_product",
#             "description": "Permanently remove a product from the catalog. Fails if the product is part of any existing order.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "product_name": {"type": "string", "description": "Name of the product to remove."},
#                 },
#                 "required": ["product_name"],
#             },
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "list_users",
#             "description": "List every registered user account, including their role and active status.",
#             "parameters": {"type": "object", "properties": {}},
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "deactivate_user",
#             "description": "Deactivate a user account, immediately revoking their access. Reversible via activate_user.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "username": {"type": "string", "description": "Username of the account to deactivate."},
#                 },
#                 "required": ["username"],
#             },
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "activate_user",
#             "description": "Reactivate a previously deactivated user account.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "username": {"type": "string", "description": "Username of the account to reactivate."},
#                 },
#                 "required": ["username"],
#             },
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "delete_user",
#             "description": "Permanently delete a user account. Fails if that user has any order history — deactivate instead in that case.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "username": {"type": "string", "description": "Username of the account to delete."},
#                 },
#                 "required": ["username"],
#             },
#         },
#     },
#     {
#     "type": "function",
#     "function": {
#         "name": "list_orders",
#         "description": "List orders, optionally filtered by status (pending, preparing, ready, completed, cancelled). Use this to see what needs to be prepared/served.",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "status": {
#                     "type": "string",
#                     "description": "Optional filter, e.g. 'pending' to see only orders not yet started.",
#                 },
#             },
#         },
#     },
# },
# {
#     "type": "function",
#     "function": {
#         "name": "update_order_status",
#         "description": "Update an order's status as it moves through preparation (pending -> preparing -> ready -> completed), or mark it cancelled.",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "order_id": {
#                     "type": "integer",
#                     "description": "The order's id.",
#                 },
#                 "new_status": {
#                     "type": "string",
#                     "description": "One of: pending, preparing, ready, completed, cancelled.",
#                 },
#             },
#             "required": ["order_id", "new_status"],
#         },
#     },
# },
# ]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_products",
            "description": "Get all available products.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_product_by_name",
            "description": "Search available products by name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The product name or keyword to search for.",
                    }
                },
                "required": ["name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_products_by_max_price",
            "description": "Get products with a price less than or equal to the specified maximum price.",
            "parameters": {
                "type": "object",
                "properties": {
                    "max_price": {
                        "type": "number",
                        "description": "Maximum product price.",
                    }
                },
                "required": ["max_price"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_products_by_min_price",
            "description": "Get products with a price greater than or equal to the specified minimum price.",
            "parameters": {
                "type": "object",
                "properties": {
                    "min_price": {
                        "type": "number",
                        "description": "Minimum product price.",
                    }
                },
                "required": ["min_price"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_to_cart",
            "description": (
                "Add a product to the current user's active shopping cart, "
                "identified by product name. If the name matches more than "
                "one product, ask the user which one they meant."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "Name or partial name of the product to add.",
                    },
                    "quantity": {
                        "type": ["integer", "null"],
                        "description": "How many units to add. Defaults to 1.",
                    },
                },
                "required": ["product_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "remove_from_cart",
            "description": (
                "Remove a product from the current user's active cart. If "
                "quantity is omitted, removes the product entirely; "
                "otherwise decreases the quantity by that amount."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "Name or partial name of the product to remove.",
                    },
                    "quantity": {
                        "type": ["integer", "null"],
                        "description": "How many units to remove. Omit to remove entirely.",
                    },
                },
                "required": ["product_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "view_cart",
            "description": (
                "Show the items currently in the current user's active cart, "
                "with prices and total."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "checkout_cart",
            "description": (
                "Place an order from everything currently in the current "
                "user's active cart."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": (
                "Look up the status and total of one of the current user's "
                "past orders by order id."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "integer",
                        "description": "The id of the order to check.",
                    }
                },
                "required": ["order_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_orders",
            "description": "List all past orders placed by the current user.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "clear_cart",
            "description": (
                "Remove everything from the current user's active cart at once, "
                "without checking out."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
]


admin_tools = [
    {
        "type": "function",
        "function": {
            "name": "add_product",
            "description": "Add a new product to the shop's menu/catalog.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The product's name.",
                    },
                    "description": {
                        "type": "string",
                        "description": "A short description of the product.",
                    },
                    "price": {
                        "type": "number",
                        "description": "The price, e.g. 4.50.",
                    },
                },
                "required": ["name", "description", "price"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_products",
            "description": "List every product currently in the shop's catalog.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_product",
            "description": (
                "Update an existing product's name, description, and/or price. "
                "Only the fields provided are changed."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "Name of the product to update.",
                    },
                    "new_name": {
                        "type": ["string", "null"],
                        "description": "New name, if changing it.",
                    },
                    "new_description": {
                        "type": ["string", "null"],
                        "description": "New description, if changing it.",
                    },
                    "new_price": {
                        "type": ["number", "null"],
                        "description": "New price, if changing it.",
                    },
                },
                "required": ["product_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "remove_product",
            "description": (
                "Permanently remove a product from the catalog. Fails if the "
                "product is part of any existing order."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "Name of the product to remove.",
                    }
                },
                "required": ["product_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_users",
            "description": (
                "List every registered user account, including their role "
                "and active status."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "deactivate_user",
            "description": (
                "Deactivate a user account, immediately revoking their access. "
                "Reversible via activate_user."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "Username of the account to deactivate.",
                    }
                },
                "required": ["username"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "activate_user",
            "description": (
                "Reactivate a previously deactivated user account."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "Username of the account to reactivate.",
                    }
                },
                "required": ["username"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_user",
            "description": (
                "Permanently delete a user account. Fails if that user has "
                "any order history — deactivate instead in that case."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "Username of the account to delete.",
                    }
                },
                "required": ["username"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_orders",
            "description": (
                "List orders, optionally filtered by status "
                "(pending, preparing, ready, out_for_delivery, delivered, "
                "cancelled). Use this to see what needs to be prepared/served."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": ["string", "null"],
                        "description": (
                            "Optional filter, e.g. 'pending' to see only "
                            "orders not yet started."
                        ),
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_order_status",
            "description": (
                "Update an order's status as it moves through preparation "
                "and delivery (pending -> preparing -> ready -> "
                "out_for_delivery -> delivered), or mark it cancelled."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "integer",
                        "description": "The order's id.",
                    },
                    "new_status": {
                        "type": "string",
                        "description": (
                            "One of: pending, preparing, ready, "
                            "out_for_delivery, delivered, cancelled."
                        ),
                    },
                },
                "required": ["order_id", "new_status"],
            },
        },
    },
]

