def get_user_avatar_color(username):
    """Generate a consistent color for user avatar based on username"""
    colors = [
        "#58D228", "#1BCCC3", "#1E79E1", "#CBE713", "#E93625",
        "#8F148F", "#C115B8", "#FD2C87", "#29D3E6", "#02591E"
    ]
    return colors[hash(username) % len(colors)]