from src.core.xvar import XVar


def manage_close(xvar: XVar) -> int:
    """Handle window close event"""
    print("Closing window...")
    xvar.mlx.mlx_loop_exit(xvar.mlx_ptr)
    return 0
