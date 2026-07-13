import streamlit as st
import numpy as np

# ----------------------------------------------------------------------
# 1. CUSTOM CSS – Glassmorphism Design with Perfect Contrast
# ----------------------------------------------------------------------
st.markdown("""
<style>
    /* Global background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }

    /* Glassmorphism card */
    .glass-card {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin: 1rem 0;
    }

    /* INPUT FIELDS - FIXED FOR VISIBILITY */
    .stNumberInput input {
        background-color: #ffffff !important; /* Pure white background */
        color: #000000 !important;             /* BLACK text for perfect readability */
        border: 2px solid #4a4a6a !important;  /* Dark border to stand out */
        border-radius: 10px !important;
        text-align: center !important;
        font-size: 1.4rem !important;
        font-weight: bold !important;
        padding: 0 !important;
        width: 60px !important;
        height: 60px !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        margin: 2px !important;
    }

    /* Input focus state */
    .stNumberInput input:focus {
        border: 2px solid #6c63ff !important;
        box-shadow: 0 0 15px rgba(108, 99, 255, 0.7) !important;
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* Buttons */
    .stButton button {
        background: rgba(108, 99, 255, 0.7) !important;
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: #fff !important;
        border-radius: 30px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3) !important;
    }

    .stButton button:hover {
        background: rgba(108, 99, 255, 0.9) !important;
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(108, 99, 255, 0.5) !important;
    }

    /* Headings and text */
    h1, h2, h3 {
        color: #fff !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }

    /* Success / error messages */
    .stAlert {
        border-radius: 15px !important;
        backdrop-filter: blur(4px) !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# 2. SUDOKU LOGIC FUNCTIONS
# ----------------------------------------------------------------------
def is_valid(board: np.ndarray, row: int, col: int, num: int) -> bool:
    """Check if placing 'num' at (row, col) is valid."""
    # Row check
    if num in board[row, :]:
        return False
    # Column check
    if num in board[:, col]:
        return False
    # 3x3 box check
    box_row, box_col = (row // 3) * 3, (col // 3) * 3
    if num in board[box_row:box_row+3, box_col:box_col+3]:
        return False
    return True

def solve_sudoku(board: np.ndarray) -> bool:
    """Backtracking solver – modifies board in-place."""
    for row in range(9):
        for col in range(9):
            if board[row, col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row, col] = num
                        if solve_sudoku(board):
                            return True
                        board[row, col] = 0  # backtrack
                return False
    return True

def is_board_valid(board: np.ndarray) -> bool:
    """Check if the initial board has no conflicts (ignoring zeros)."""
    for row in range(9):
        for col in range(9):
            val = board[row, col]
            if val == 0:
                continue
            # Temporarily set to 0 to avoid self-conflict
            board[row, col] = 0
            if not is_valid(board, row, col, val):
                board[row, col] = val
                return False
            board[row, col] = val
    return True

# ----------------------------------------------------------------------
# 3. STREAMLIT APP
# ----------------------------------------------------------------------
def main():
    st.title("🧩 Glass Sudoku Solver")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("""
    Enter the puzzle below. Use **0** for empty cells.  
    Click **Solve** to get the answer.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # Initialize session state for the board
    if "board" not in st.session_state:
        # Default sample puzzle matching the SUDOKU image exactly
        sample = np.array([
            [8, 0, 6, 0, 3, 0, 0, 9, 0],
            [0, 4, 0, 0, 1, 0, 0, 6, 8],
            [2, 0, 0, 8, 7, 0, 0, 0, 5],
            [1, 0, 8, 0, 0, 5, 0, 2, 0],
            [0, 3, 0, 1, 0, 0, 0, 0, 5],
            [7, 0, 5, 0, 3, 0, 9, 0, 0],
            [0, 2, 1, 0, 0, 7, 0, 4, 0],
            [6, 0, 0, 0, 2, 0, 8, 0, 0],
            [0, 8, 7, 6, 0, 4, 0, 0, 3]
        ])
        st.session_state.board = sample

    # Input grid – 9 rows, 9 columns
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    for row in range(9):
        row_cols = st.columns(9)
        for col in range(9):
            with row_cols[col]:
                val = st.number_input(
                    label=f"r{row+1}c{col+1}",
                    min_value=0,
                    max_value=9,
                    value=int(st.session_state.board[row, col]),
                    step=1,
                    key=f"cell_{row}_{col}",
                    label_visibility="collapsed"
                )
                # Update session state board (key is updated on change)
                st.session_state.board[row, col] = val
    st.markdown('</div>', unsafe_allow_html=True)

    # Buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🧹 Clear Board"):
            st.session_state.board = np.zeros((9, 9), dtype=int)
            st.rerun()
    with col2:
        if st.button("📥 Load Sample"):
            sample = np.array([
                [8, 0, 6, 0, 3, 0, 0, 9, 0],
                [0, 4, 0, 0, 1, 0, 0, 6, 8],
                [2, 0, 0, 8, 7, 0, 0, 0, 5],
                [1, 0, 8, 0, 0, 5, 0, 2, 0],
                [0, 3, 0, 1, 0, 0, 0, 0, 5],
                [7, 0, 5, 0, 3, 0, 9, 0, 0],
                [0, 2, 1, 0, 0, 7, 0, 4, 0],
                [6, 0, 0, 0, 2, 0, 8, 0, 0],
                [0, 8, 7, 6, 0, 4, 0, 0, 3]
            ])
            st.session_state.board = sample
            st.rerun()
    with col3:
        solve_clicked = st.button("🚀 Solve")

    # Solving logic
    if solve_clicked:
        board = st.session_state.board.copy()
        # Check validity of initial puzzle
        if not is_board_valid(board):
            st.error("❌ The puzzle contains conflicts (duplicate numbers in a row/column/box). Please fix it.")
        else:
            if solve_sudoku(board):
                st.session_state.board = board
                st.success("✅ Puzzle solved successfully!")
            else:
                st.error("❌ No solution exists for this puzzle.")

    # Display the solved board
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Current Board")
    
    # Render as a table with black text on white background
    for row in range(9):
        cols = st.columns(9)
        for col in range(9):
            val = st.session_state.board[row, col]
            with cols[col]:
                if val == 0:
                    st.markdown(
                        '<div style="background-color: #ffffff; color: #000000; border-radius: 8px; padding: 10px 0; text-align: center; font-weight: bold; font-size: 1.2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"> </div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div style="background-color: #ffffff; color: #000000; border-radius: 8px; padding: 10px 0; text-align: center; font-weight: bold; font-size: 1.2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">{val}</div>',
                        unsafe_allow_html=True
                    )
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
