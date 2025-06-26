def get_user_avatar_color(username):
    """Generate a consistent color for user avatar based on username"""
    colors = [
        "#2C377D", "#196433", "#0F4078", "#6B7625", "#50201B",
        "#674D67", "#751270", "#681237", "#45686C", "#9A5817"
    ]
    return colors[hash(username) % len(colors)]