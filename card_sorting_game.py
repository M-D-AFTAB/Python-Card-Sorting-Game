import tkinter as tk
from tkinter import messagebox
import random
import time
import math

# ==========================================
# CARD SORTING CHALLENGE (5-ALGORITHM EDITION)
# Python + DSA + Tkinter GUI
# ==========================================

BG = "#0B1F1A"
PANEL = "#14352B"
GREEN = "#1E8449"
BRIGHT_GREEN = "#2ECC71"
GOLD = "#F4C542"
ORANGE = "#F39C12"
CYAN = "#00D2FF"
PURPLE = "#AF7AC5"
PINK = "#FF4081"
WHITE = "#FFFFFF"
RED = "#E74C3C"
MUTED = "#B8CEC5"

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]

SUIT_SYMBOLS = {
    "Hearts": "♥",
    "Diamonds": "♦",
    "Clubs": "♣",
    "Spades": "♠"
}

RANKS = {
    1: "A", 2: "2", 3: "3", 4: "4",
    5: "5", 6: "6", 7: "7", 8: "8",
    9: "9", 10: "10", 11: "J",
    12: "Q", 13: "K"
}

CARD_WIDTH = 82
CARD_HEIGHT = 112


# ==========================================
# DECK FUNCTIONS
# ==========================================

def create_deck():
    return [
        (value, suit)
        for suit in SUITS
        for value in range(1, 14)
    ]


def card_name(card):
    value, suit = card
    return f"{RANKS[value]} of {suit}"


def card_text(card):
    value, suit = card
    return f"{RANKS[value]}{SUIT_SYMBOLS[suit]}"


def card_color(card):
    if card[1] in ("Hearts", "Diamonds"):
        return RED
    return "#17202A"


# ==========================================
# SORTING ALGORITHMS (STEP GENERATORS)
# ==========================================

def bubble_sort(cards):
    cards = cards.copy()
    n = len(cards)
    comparisons = 0
    movements = 0
    sorted_indices = set()

    for i in range(n):
        swapped = False

        for j in range(n - i - 1):
            comparisons += 1
            yield {
                "action": "compare",
                "indices": (j, j + 1),
                "cards": cards.copy(),
                "comparisons": comparisons,
                "movements": movements,
                "sorted": sorted_indices.copy(),
                "status": f"Bubble Sort: Comparing {card_text(cards[j])} and {card_text(cards[j + 1])}"
            }

            if cards[j][0] > cards[j + 1][0]:
                cards[j], cards[j + 1] = cards[j + 1], cards[j]
                movements += 1
                swapped = True

                yield {
                    "action": "swap",
                    "indices": (j, j + 1),
                    "cards": cards.copy(),
                    "comparisons": comparisons,
                    "movements": movements,
                    "sorted": sorted_indices.copy(),
                    "status": f"Bubble Sort: Swapping {card_text(cards[j + 1])} ↔ {card_text(cards[j])}"
                }

        sorted_indices.add(n - 1 - i)

        if not swapped:
            for k in range(n - i - 1):
                sorted_indices.add(k)
            break

    yield {
        "action": "done",
        "cards": cards.copy(),
        "comparisons": comparisons,
        "movements": movements,
        "sorted": set(range(n)),
        "status": "Bubble Sort complete!"
    }


def selection_sort(cards):
    cards = cards.copy()
    n = len(cards)
    comparisons = 0
    movements = 0
    sorted_indices = set()

    for i in range(n):
        minimum = i

        yield {
            "action": "select_min",
            "min_idx": minimum,
            "old_min": None,
            "cards": cards.copy(),
            "comparisons": comparisons,
            "movements": movements,
            "sorted": sorted_indices.copy(),
            "status": f"Selection Sort: Setting initial minimum to {card_text(cards[minimum])}"
        }

        for j in range(i + 1, n):
            comparisons += 1
            yield {
                "action": "scan",
                "scan_idx": j,
                "min_idx": minimum,
                "cards": cards.copy(),
                "comparisons": comparisons,
                "movements": movements,
                "sorted": sorted_indices.copy(),
                "status": f"Selection Sort: Comparing {card_text(cards[j])} with minimum {card_text(cards[minimum])}"
            }

            if cards[j][0] < cards[minimum][0]:
                old_min = minimum
                minimum = j
                yield {
                    "action": "select_min",
                    "min_idx": minimum,
                    "old_min": old_min,
                    "cards": cards.copy(),
                    "comparisons": comparisons,
                    "movements": movements,
                    "sorted": sorted_indices.copy(),
                    "status": f"Selection Sort: New minimum found → {card_text(cards[minimum])}"
                }

        if minimum != i:
            cards[i], cards[minimum] = cards[minimum], cards[i]
            movements += 1
            yield {
                "action": "swap",
                "indices": (i, minimum),
                "cards": cards.copy(),
                "comparisons": comparisons,
                "movements": movements,
                "sorted": sorted_indices.copy(),
                "status": f"Selection Sort: Swapping minimum {card_text(cards[i])} into slot {i + 1}"
            }
        else:
            yield {
                "action": "lower_min",
                "min_idx": minimum,
                "cards": cards.copy(),
                "comparisons": comparisons,
                "movements": movements,
                "sorted": sorted_indices.copy(),
                "status": f"Selection Sort: {card_text(cards[i])} is already in the correct position"
            }

        sorted_indices.add(i)

    yield {
        "action": "done",
        "cards": cards.copy(),
        "comparisons": comparisons,
        "movements": movements,
        "sorted": set(range(n)),
        "status": "Selection Sort complete!"
    }


def insertion_sort(cards):
    cards = cards.copy()
    n = len(cards)
    comparisons = 0
    movements = 0
    sorted_indices = {0}

    for i in range(1, n):
        current = cards[i]
        j = i - 1

        yield {
            "action": "lift_key",
            "key_idx": i,
            "cards": cards.copy(),
            "comparisons": comparisons,
            "movements": movements,
            "sorted": sorted_indices.copy(),
            "status": f"Insertion Sort: Lifting key card {card_text(current)}"
        }

        while j >= 0:
            comparisons += 1
            yield {
                "action": "compare_key",
                "compare_idx": j,
                "key_idx": j + 1,
                "cards": cards.copy(),
                "comparisons": comparisons,
                "movements": movements,
                "sorted": sorted_indices.copy(),
                "status": f"Insertion Sort: Comparing {card_text(cards[j])} with key {card_text(current)}"
            }

            if cards[j][0] > current[0]:
                cards[j], cards[j + 1] = cards[j + 1], cards[j]
                movements += 1

                yield {
                    "action": "shift_right",
                    "from_idx": j,
                    "to_idx": j + 1,
                    "cards": cards.copy(),
                    "comparisons": comparisons,
                    "movements": movements,
                    "sorted": sorted_indices.copy(),
                    "status": f"Insertion Sort: Shifting {card_text(cards[j + 1])} right"
                }
                j -= 1
            else:
                break

        sorted_indices.add(i)
        yield {
            "action": "drop_key",
            "key_idx": j + 1,
            "cards": cards.copy(),
            "comparisons": comparisons,
            "movements": movements,
            "sorted": sorted_indices.copy(),
            "status": f"Insertion Sort: Inserting {card_text(current)} into slot {j + 2}"
        }

    yield {
        "action": "done",
        "cards": cards.copy(),
        "comparisons": comparisons,
        "movements": movements,
        "sorted": set(range(n)),
        "status": "Insertion Sort complete!"
    }


def quick_sort(cards):
    cards = cards.copy()
    n = len(cards)
    comparisons = 0
    movements = 0
    sorted_indices = set()

    def _quick_sort(low, high):
        nonlocal comparisons, movements

        if low > high:
            return

        if low == high:
            sorted_indices.add(low)
            yield {
                "action": "mark_sorted",
                "index": low,
                "cards": cards.copy(),
                "comparisons": comparisons,
                "movements": movements,
                "sorted": sorted_indices.copy(),
                "status": f"Quick Sort: {card_text(cards[low])} locked in sorted position"
            }
            return

        pivot = cards[high]
        yield {
            "action": "pivot_lift",
            "pivot_idx": high,
            "low": low,
            "high": high,
            "cards": cards.copy(),
            "comparisons": comparisons,
            "movements": movements,
            "sorted": sorted_indices.copy(),
            "status": f"Quick Sort: Partitioning [{low + 1}..{high + 1}] around pivot {card_text(pivot)}"
        }

        i = low - 1

        for j in range(low, high):
            comparisons += 1
            yield {
                "action": "pivot_compare",
                "scan_idx": j,
                "pivot_idx": high,
                "bound_idx": i if i >= low else None,
                "cards": cards.copy(),
                "comparisons": comparisons,
                "movements": movements,
                "sorted": sorted_indices.copy(),
                "status": f"Quick Sort: Comparing {card_text(cards[j])} with pivot {card_text(pivot)}"
            }

            if cards[j][0] <= pivot[0]:
                i += 1
                if i != j:
                    cards[i], cards[j] = cards[j], cards[i]
                    movements += 1
                    yield {
                        "action": "pivot_swap",
                        "indices": (i, j),
                        "pivot_idx": high,
                        "cards": cards.copy(),
                        "comparisons": comparisons,
                        "movements": movements,
                        "sorted": sorted_indices.copy(),
                        "status": f"Quick Sort: Moving {card_text(cards[i])} left of partition boundary"
                    }

        pivot_final = i + 1
        sorted_indices.add(pivot_final)

        if pivot_final != high:
            cards[pivot_final], cards[high] = cards[high], cards[pivot_final]
            movements += 1
            yield {
                "action": "swap",
                "indices": (pivot_final, high),
                "cards": cards.copy(),
                "comparisons": comparisons,
                "movements": movements,
                "sorted": sorted_indices.copy(),
                "status": f"Quick Sort: Placing pivot {card_text(cards[pivot_final])} into sorted slot {pivot_final + 1}"
            }
        else:
            yield {
                "action": "lower_min",
                "min_idx": high,
                "cards": cards.copy(),
                "comparisons": comparisons,
                "movements": movements,
                "sorted": sorted_indices.copy(),
                "status": f"Quick Sort: Pivot {card_text(cards[high])} is already in sorted slot {high + 1}"
            }

        yield from _quick_sort(low, pivot_final - 1)
        yield from _quick_sort(pivot_final + 1, high)

    yield from _quick_sort(0, n - 1)

    yield {
        "action": "done",
        "cards": cards.copy(),
        "comparisons": comparisons,
        "movements": movements,
        "sorted": set(range(n)),
        "status": "Quick Sort complete!"
    }


def merge_sort(cards):
    cards = cards.copy()
    n = len(cards)
    comparisons = 0
    movements = 0
    sorted_indices = set()

    def _merge_sort(left, right):
        nonlocal comparisons, movements

        if left >= right:
            return

        mid = (left + right) // 2
        yield from _merge_sort(left, mid)
        yield from _merge_sort(mid + 1, right)

        # Lift both sorted halves into the upper staging lane
        yield {
            "action": "merge_lift",
            "left": left,
            "mid": mid,
            "right": right,
            "cards": cards.copy(),
            "comparisons": comparisons,
            "movements": movements,
            "sorted": sorted_indices.copy(),
            "status": f"Merge Sort: Merging subarrays [{left + 1}..{mid + 1}] and [{mid + 2}..{right + 1}]"
        }

        l_idx = left
        r_idx = mid + 1
        k = left
        merged_cards = []
        merged_order = []
        dropped = set()

        while l_idx <= mid and r_idx <= right:
            comparisons += 1
            yield {
                "action": "merge_compare",
                "l_idx": l_idx,
                "r_idx": r_idx,
                "left": left,
                "mid": mid,
                "right": right,
                "dropped": dropped.copy(),
                "cards": cards.copy(),
                "comparisons": comparisons,
                "movements": movements,
                "sorted": sorted_indices.copy(),
                "status": f"Merge Sort: Comparing {card_text(cards[l_idx])} (Left) vs {card_text(cards[r_idx])} (Right)"
            }

            if cards[l_idx][0] <= cards[r_idx][0]:
                winner = l_idx
                l_idx += 1
            else:
                winner = r_idx
                r_idx += 1

            movements += 1
            merged_cards.append(cards[winner])
            merged_order.append(winner)
            dropped.add(winner)

            yield {
                "action": "merge_drop",
                "from_idx": winner,
                "to_slot": k,
                "left": left,
                "mid": mid,
                "right": right,
                "dropped": dropped.copy(),
                "cards": cards.copy(),
                "comparisons": comparisons,
                "movements": movements,
                "sorted": sorted_indices.copy(),
                "status": f"Merge Sort: Placing {card_text(cards[winner])} into merged slot {k + 1}"
            }
            k += 1

        while l_idx <= mid:
            winner = l_idx
            l_idx += 1
            movements += 1
            merged_cards.append(cards[winner])
            merged_order.append(winner)
            dropped.add(winner)

            yield {
                "action": "merge_drop",
                "from_idx": winner,
                "to_slot": k,
                "left": left,
                "mid": mid,
                "right": right,
                "dropped": dropped.copy(),
                "cards": cards.copy(),
                "comparisons": comparisons,
                "movements": movements,
                "sorted": sorted_indices.copy(),
                "status": f"Merge Sort: Placing remaining left card {card_text(cards[winner])} into slot {k + 1}"
            }
            k += 1

        while r_idx <= right:
            winner = r_idx
            r_idx += 1
            movements += 1
            merged_cards.append(cards[winner])
            merged_order.append(winner)
            dropped.add(winner)

            yield {
                "action": "merge_drop",
                "from_idx": winner,
                "to_slot": k,
                "left": left,
                "mid": mid,
                "right": right,
                "dropped": dropped.copy(),
                "cards": cards.copy(),
                "comparisons": comparisons,
                "movements": movements,
                "sorted": sorted_indices.copy(),
                "status": f"Merge Sort: Placing remaining right card {card_text(cards[winner])} into slot {k + 1}"
            }
            k += 1

        cards[left:right + 1] = merged_cards
        if left == 0 and right == n - 1:
            for idx in range(n):
                sorted_indices.add(idx)

        yield {
            "action": "merge_commit",
            "left": left,
            "right": right,
            "order": merged_order,
            "cards": cards.copy(),
            "comparisons": comparisons,
            "movements": movements,
            "sorted": sorted_indices.copy(),
            "status": f"Merge Sort: Subarray [{left + 1}..{right + 1}] merged!"
        }

    yield from _merge_sort(0, n - 1)

    yield {
        "action": "done",
        "cards": cards.copy(),
        "comparisons": comparisons,
        "movements": movements,
        "sorted": set(range(n)),
        "status": "Merge Sort complete!"
    }


# ==========================================
# MAIN APPLICATION
# ==========================================

class CardSortingGame:

    def __init__(self, root):
        self.root = root
        self.root.title("Card Sorting Challenge | Python + DSA")
        self.root.geometry("1120x830")
        self.root.minsize(960, 720)
        self.root.configure(bg=BG)

        self.cards = []
        self.score = 0
        self.busy = False
        self.drag_index = None
        self.card_items = []
        self.card_positions = []
        self.sorted_indices = set()

        self.algorithm = None
        self.sort_generator = None
        self.comparisons = 0
        self.movements = 0
        self.start_time = 0
        self.speed_multiplier = 1.25

        self.build_ui()
        self.root.after(100, lambda: self.new_game(animate=True))

    # ======================================
    # USER INTERFACE
    # ======================================

    def build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=25, pady=(14, 6))

        tk.Label(
            header,
            text="♠ CARD SORTING CHALLENGE ♥",
            font=("Arial", 23, "bold"),
            bg=BG,
            fg=GOLD
        ).pack()

        tk.Label(
            header,
            text="Interactive Sorting & Shuffle Visualizer • Python + DSA",
            font=("Arial", 11),
            bg=BG,
            fg=MUTED
        ).pack(pady=3)

        # Score & Status panel
        score_panel = tk.Frame(self.root, bg=PANEL, padx=15, pady=10)
        score_panel.pack(fill="x", padx=25, pady=6)

        self.score_label = tk.Label(
            score_panel,
            text="🏆 SCORE: 0",
            font=("Arial", 12, "bold"),
            bg=PANEL,
            fg=GOLD
        )
        self.score_label.pack(side="left")

        self.status_label = tk.Label(
            score_panel,
            text="Welcome! Sort the cards by rank.",
            font=("Arial", 11, "bold"),
            bg=PANEL,
            fg=WHITE
        )
        self.status_label.pack(side="right")

        # Card canvas area (extra height for 2-lane Merge Sort & Quick Sort pivots)
        self.canvas = tk.Canvas(
            self.root,
            bg="#145A32",
            height=295,
            highlightthickness=2,
            highlightbackground=GOLD
        )
        self.canvas.pack(fill="x", padx=25, pady=10)

        # Color Legend bar
        legend_frame = tk.Frame(self.root, bg=BG)
        legend_frame.pack(pady=(0, 6))

        legend_items = [
            (GOLD, "Comparing / Scan"),
            (RED, "Swapping / Shifting"),
            (CYAN, "Min / Left Half"),
            (PURPLE, "Key / Right Half"),
            (PINK, "Quick Sort Pivot"),
            (BRIGHT_GREEN, "Sorted")
        ]
        for color, label in legend_items:
            swatch = tk.Frame(legend_frame, bg=color, width=13, height=13)
            swatch.pack(side="left", padx=(10, 4))
            tk.Label(
                legend_frame,
                text=label,
                font=("Arial", 9, "bold"),
                bg=BG,
                fg=MUTED
            ).pack(side="left", padx=(0, 6))

        # Drag, drop, and resize bindings
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag_card)
        self.canvas.bind("<ButtonRelease-1>", self.drop_card)
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        # Main game buttons
        button_frame = tk.Frame(self.root, bg=BG)
        button_frame.pack(pady=5)

        self.make_button(
            button_frame, "🎲 New Cards",
            lambda: self.new_game(animate=True), GREEN
        ).grid(row=0, column=0, padx=5, pady=4)

        self.make_button(
            button_frame, "🏆 Check Order",
            self.check_order, "#2874A6"
        ).grid(row=0, column=1, padx=5, pady=4)

        self.make_button(
            button_frame, "🔀 Shuffle",
            self.shuffle_game, "#7D3C98"
        ).grid(row=0, column=2, padx=5, pady=4)

        # Sorting algorithms & speed control
        algo_frame = tk.Frame(self.root, bg=BG)
        algo_frame.pack(pady=6)

        tk.Label(
            algo_frame,
            text="SORTING VISUALIZER",
            font=("Arial", 12, "bold"),
            bg=BG,
            fg=GOLD
        ).grid(row=0, column=0, columnspan=6, pady=6)

        self.make_button(
            algo_frame, "Bubble Sort",
            lambda: self.start_sort("Bubble Sort"),
            "#C0392B"
        ).grid(row=1, column=0, padx=5)

        self.make_button(
            algo_frame, "Selection Sort",
            lambda: self.start_sort("Selection Sort"),
            "#B9770E"
        ).grid(row=1, column=1, padx=5)

        self.make_button(
            algo_frame, "Insertion Sort",
            lambda: self.start_sort("Insertion Sort"),
            "#148F77"
        ).grid(row=1, column=2, padx=5)

        self.make_button(
            algo_frame, "Quick Sort",
            lambda: self.start_sort("Quick Sort"),
            "#AD1457"
        ).grid(row=1, column=3, padx=5)

        self.make_button(
            algo_frame, "Merge Sort",
            lambda: self.start_sort("Merge Sort"),
            "#5B2C6F"
        ).grid(row=1, column=4, padx=5)

        # Animation speed slider
        speed_box = tk.Frame(algo_frame, bg=PANEL, padx=10, pady=2)
        speed_box.grid(row=1, column=5, padx=8)

        tk.Label(
            speed_box,
            text="⚡ Speed:",
            font=("Arial", 9, "bold"),
            bg=PANEL,
            fg=GOLD
        ).pack(side="left", padx=(0, 6))

        self.speed_scale = tk.Scale(
            speed_box,
            from_=0.5,
            to=3.0,
            resolution=0.25,
            orient="horizontal",
            length=105,
            bg=PANEL,
            fg=WHITE,
            highlightthickness=0,
            troughcolor=BG,
            activebackground=GOLD,
            font=("Arial", 8),
            command=self.update_speed
        )
        self.speed_scale.set(1.25)
        self.speed_scale.pack(side="left")

        # Statistics panel
        stats = tk.Frame(self.root, bg=PANEL, padx=20, pady=10)
        stats.pack(fill="x", padx=25, pady=8)

        for col in range(3):
            stats.grid_columnconfigure(col, weight=1)

        self.comparison_label = tk.Label(
            stats,
            text="Comparisons: 0",
            font=("Arial", 11, "bold"),
            bg=PANEL,
            fg=WHITE
        )
        self.comparison_label.grid(row=0, column=0, padx=18)

        self.movement_label = tk.Label(
            stats,
            text="Swaps/Shifts: 0",
            font=("Arial", 11, "bold"),
            bg=PANEL,
            fg=WHITE
        )
        self.movement_label.grid(row=0, column=1, padx=18)

        self.time_label = tk.Label(
            stats,
            text="Time: 0.000000 s",
            font=("Arial", 11, "bold"),
            bg=PANEL,
            fg=WHITE
        )
        self.time_label.grid(row=0, column=2, padx=18)

        # Bottom controls
        footer = tk.Frame(self.root, bg=BG)
        footer.pack(pady=6)

        self.make_button(
            footer, "📊 Compare All 5 Algorithms",
            self.compare_algorithms, "#34495E"
        ).pack(side="left", padx=8)

        self.make_button(
            footer, "🚪 Exit",
            self.root.destroy, "#566573"
        ).pack(side="left", padx=8)

        tk.Label(
            self.root,
            text="DSA Concepts: Bubble Sort • Selection Sort • Insertion Sort • Quick Sort • Merge Sort",
            font=("Arial", 9),
            bg=BG,
            fg=MUTED
        ).pack(side="bottom", pady=6)

    def make_button(self, parent, text, command, color):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 10, "bold"),
            bg=color,
            fg=WHITE,
            activebackground=GOLD,
            activeforeground=BG,
            relief="flat",
            padx=12,
            pady=8,
            cursor="hand2"
        )

    def update_speed(self, val):
        self.speed_multiplier = float(val)

    def on_canvas_resize(self, event):
        if not self.busy and self.cards:
            self.draw_cards()

    # ======================================
    # CARD GEOMETRY & DRAWING
    # ======================================

    def compute_layout(self):
        width = max(self.canvas.winfo_width(), 920)
        height = max(self.canvas.winfo_height(), 295)
        count = max(1, len(self.cards))

        card_width = min(
            CARD_WIDTH,
            max(48, (width - 40) // count - 10)
        )
        card_height = int(card_width * CARD_HEIGHT / CARD_WIDTH)
        gap = (width - count * card_width) // (count + 1)

        # Extra top headroom for lifted Merge Sort subarrays and Quick Sort pivots
        base_y = (height - card_height) // 2 + 26
        base_y = max(76, base_y)

        slots = []
        for i in range(count):
            x = gap + i * (card_width + gap)
            slots.append((x, base_y, card_width, card_height))

        return slots, width, height

    def draw_cards(self):
        self.canvas.delete("all")
        self.card_items = []
        self.card_positions = []

        if not self.cards:
            return

        slots, _, _ = self.compute_layout()

        for index, card in enumerate(self.cards):
            x, y, card_width, card_height = slots[index]
            is_sorted = index in self.sorted_indices

            outline = BRIGHT_GREEN if is_sorted else "#D5D8DC"
            outline_width = 3 if is_sorted else 2
            fill_color = "#EAFAF1" if is_sorted else "#FDFEFE"

            # Drop shadow
            shadow = self.canvas.create_rectangle(
                x + 4, y + 5,
                x + card_width + 4, y + card_height + 5,
                fill="#0D3B22",
                outline=""
            )

            # Card body
            rect = self.canvas.create_rectangle(
                x, y,
                x + card_width, y + card_height,
                fill=fill_color,
                outline=outline,
                width=outline_width
            )

            symbol = SUIT_SYMBOLS[card[1]]
            color = card_color(card)
            value = RANKS[card[0]]

            top_text = self.canvas.create_text(
                x + 8,
                y + 7,
                text=value,
                anchor="nw",
                font=("Arial", max(10, card_width // 5), "bold"),
                fill=color
            )

            center_text = self.canvas.create_text(
                x + card_width // 2,
                y + card_height // 2,
                text=symbol,
                font=("Arial", max(20, card_width // 2), "bold"),
                fill=color
            )

            bottom_text = self.canvas.create_text(
                x + card_width - 8,
                y + card_height - 7,
                text=f"{value}{symbol}",
                anchor="se",
                font=("Arial", max(9, card_width // 6), "bold"),
                fill=color
            )

            # Floating status badge above card
            badge_text = self.canvas.create_text(
                x + card_width // 2,
                y - 11,
                text="✓" if is_sorted else "",
                font=("Arial", 9, "bold"),
                fill=BRIGHT_GREEN
            )

            self.card_items.append(
                (shadow, rect, top_text, center_text, bottom_text, badge_text)
            )
            self.card_positions.append([x, y, card_width, card_height])

    # ======================================
    # LOW-LEVEL ANIMATION HELPERS
    # ======================================

    def move_card_to(self, index, target_x, target_y):
        if index >= len(self.card_items):
            return
        cur_x, cur_y, w, h = self.card_positions[index]
        dx = target_x - cur_x
        dy = target_y - cur_y

        for item_id in self.card_items[index]:
            self.canvas.move(item_id, dx, dy)

        self.card_positions[index][0] = target_x
        self.card_positions[index][1] = target_y

    def raise_card_z(self, index):
        if index >= len(self.card_items):
            return
        for item_id in self.card_items[index]:
            self.canvas.tag_raise(item_id)

    def style_card(self, index, outline="#D5D8DC", width=2, fill="#FDFEFE", badge="", badge_color=GOLD):
        if index >= len(self.card_items):
            return
        _, rect, _, _, _, badge_item = self.card_items[index]
        self.canvas.itemconfig(rect, outline=outline, width=width, fill=fill)
        self.canvas.itemconfig(badge_item, text=badge, fill=badge_color)

    def refresh_sorted_styles(self, sorted_set, active_badges=None):
        active_badges = active_badges or {}
        for idx in range(len(self.card_items)):
            if idx in active_badges:
                color, fill, badge_str = active_badges[idx]
                self.style_card(idx, outline=color, width=4, fill=fill, badge=badge_str, badge_color=color)
            elif idx in sorted_set:
                self.style_card(idx, outline=BRIGHT_GREEN, width=3, fill="#EAFAF1", badge="✓", badge_color=BRIGHT_GREEN)
            else:
                self.style_card(idx, outline="#D5D8DC", width=2, fill="#FDFEFE", badge="")

    def build_merge_badges(self, left, mid, right, dropped, extra=None):
        badges = {}
        for idx in range(left, right + 1):
            if idx in dropped:
                badges[idx] = (BRIGHT_GREEN, "#EAFAF1", "MERGED")
            elif idx <= mid:
                badges[idx] = (CYAN, "#EBF5FB", "LEFT")
            else:
                badges[idx] = (PURPLE, "#F5EEF8", "RIGHT")
        if extra:
            badges.update(extra)
        return badges

    def animate_trajectories(self, trajectories, frames, on_complete):
        """
        Smoothly interpolates multiple cards simultaneously.
        trajectories: list of (card_idx, start_x, start_y, end_x, end_y, arc_height)
        """
        total_frames = max(3, int(frames / self.speed_multiplier))

        def step_frame(frame_idx):
            if not self.root.winfo_exists():
                return

            t = frame_idx / total_frames
            ease = t * t * (3 - 2 * t)

            for idx, sx, sy, ex, ey, arc in trajectories:
                nx = sx + (ex - sx) * ease
                ny = sy + (ey - sy) * ease - arc * math.sin(math.pi * t)
                self.move_card_to(idx, nx, ny)

            if frame_idx < total_frames:
                self.root.after(16, lambda: step_frame(frame_idx + 1))
            else:
                for idx, _, _, ex, ey, _ in trajectories:
                    self.move_card_to(idx, ex, ey)
                on_complete()

        step_frame(1)

    # ======================================
    # SHUFFLE & DEAL ANIMATION
    # ======================================

    def animate_shuffle_and_deal(self, new_deck=False):
        if self.busy:
            return

        self.busy = True
        self.sorted_indices.clear()
        self.comparisons = 0
        self.movements = 0
        self.time_label.config(text="Time: 0.000000 s")
        self.update_stats()

        if not self.cards:
            self.cards = random.sample(create_deck(), 8)
            self.draw_cards()

        slots, canvas_w, _ = self.compute_layout()
        card_w, card_h = slots[0][2], slots[0][3]
        base_y = slots[0][1]
        center_x = (canvas_w - card_w) // 2

        self.status_label.config(
            text="🎲 Dealing new cards..." if new_deck else "🔀 Riffle shuffling cards..."
        )

        gather_traj = []
        for idx in range(len(self.cards)):
            sx, sy, _, _ = self.card_positions[idx]
            offset = (idx - len(self.cards) // 2) * 2
            gather_traj.append((idx, sx, sy, center_x + offset, base_y, -15))

        def start_riffle(riffle_count=2):
            if riffle_count <= 0:
                finish_deal()
                return

            split_traj = []
            for idx in range(len(self.cards)):
                sx, sy, _, _ = self.card_positions[idx]
                direction = -1 if idx % 2 == 0 else 1
                tx = center_x + direction * (card_w * 0.75)
                self.style_card(idx, outline=GOLD, width=3, fill="#FDFEFE")
                split_traj.append((idx, sx, sy, tx, base_y, 12 * direction))

            def merge_riffle():
                order = list(range(len(self.cards)))
                random.shuffle(order)
                for idx in order:
                    self.raise_card_z(idx)

                merge_traj = []
                for idx in range(len(self.cards)):
                    sx, sy, _, _ = self.card_positions[idx]
                    merge_traj.append((idx, sx, sy, center_x, base_y, 0))

                self.animate_trajectories(
                    merge_traj, 8,
                    lambda: start_riffle(riffle_count - 1)
                )

            self.animate_trajectories(split_traj, 8, merge_riffle)

        def finish_deal():
            if new_deck:
                self.cards = random.sample(create_deck(), 8)
            else:
                random.shuffle(self.cards)

            self.draw_cards()
            for idx in range(len(self.cards)):
                self.move_card_to(idx, center_x, base_y)

            deal_traj = []
            for idx in range(len(self.cards)):
                tx, ty, _, _ = slots[idx]
                arc = 28 + idx * 3
                deal_traj.append((idx, center_x, base_y, tx, ty, arc))

            def on_deal_finished():
                self.busy = False
                self.status_label.config(
                    text="New cards dealt! Arrange them in ascending order."
                    if new_deck else "Cards shuffled! Ready to play or visualize."
                )

            self.animate_trajectories(deal_traj, 16, on_deal_finished)

        self.animate_trajectories(gather_traj, 12, lambda: start_riffle(2))

    def celebrate_wave(self, on_done=None):
        """Runs a sequential upward hop across all sorted cards."""
        slots, _, _ = self.compute_layout()

        def wave_card(idx):
            if not self.root.winfo_exists():
                return
            if idx >= len(self.cards):
                if on_done:
                    on_done()
                return

            x, y, _, _ = slots[idx]
            self.style_card(idx, outline=GOLD, width=4, fill="#EAFAF1", badge="★", badge_color=GOLD)

            self.animate_trajectories(
                [(idx, x, y, x, y, 28)],
                6,
                lambda: self.style_card(
                    idx, outline=BRIGHT_GREEN, width=3, fill="#EAFAF1", badge="✓", badge_color=BRIGHT_GREEN
                )
            )
            self.root.after(int(55 / self.speed_multiplier), lambda: wave_card(idx + 1))

        wave_card(0)

    # ======================================
    # GAME FUNCTIONS
    # ======================================

    def new_game(self, animate=True):
        if self.busy:
            return
        if animate:
            self.animate_shuffle_and_deal(new_deck=True)
        else:
            self.sorted_indices.clear()
            self.cards = random.sample(create_deck(), 8)
            self.comparisons = 0
            self.movements = 0
            self.update_stats()
            self.draw_cards()

    def shuffle_game(self):
        if self.busy:
            return
        self.animate_shuffle_and_deal(new_deck=False)

    def check_order(self):
        if self.busy:
            return

        values = [card[0] for card in self.cards]

        if values == sorted(values):
            self.busy = True
            self.sorted_indices = set(range(len(self.cards)))
            self.score += 100
            self.score_label.config(text=f"🏆 SCORE: {self.score}")
            self.status_label.config(text="🎉 Correct! You earned 100 points!")

            def show_congrats():
                self.busy = False
                messagebox.showinfo(
                    "Congratulations!",
                    "Excellent work!\n\n"
                    "Your cards are sorted correctly.\n"
                    "You earned 100 points!"
                )

            self.celebrate_wave(on_done=show_congrats)
        else:
            self.status_label.config(text="Not sorted yet. Try rearranging the cards!")
            messagebox.showwarning(
                "Keep Trying!",
                "The cards are not in ascending order.\n\n"
                "Drag the cards to arrange them from lowest to highest."
            )

    # ======================================
    # DRAG AND DROP
    # ======================================

    def start_drag(self, event):
        if self.busy:
            return

        for index, (x, y, width, height) in enumerate(self.card_positions):
            if x <= event.x <= x + width and y <= event.y <= y + height:
                self.drag_index = index
                self.raise_card_z(index)
                self.style_card(index, outline=GOLD, width=4, fill="#FEF9E7", badge="DRAG", badge_color=GOLD)
                return

    def drag_card(self, event):
        if self.drag_index is None or self.busy:
            return

        index = self.drag_index
        if index >= len(self.card_items):
            return

        _, _, width, height = self.card_positions[index]
        target_x = event.x - width // 2
        target_y = event.y - height // 2
        self.move_card_to(index, target_x, target_y)

    def drop_card(self, event):
        if self.drag_index is None or self.busy:
            return

        source = self.drag_index
        self.drag_index = None
        target = None

        slots, _, _ = self.compute_layout()

        for index, (x, y, width, height) in enumerate(slots):
            if index != source and x <= event.x <= x + width and y - 40 <= event.y <= y + height + 40:
                target = index
                break

        if target is not None and target != source:
            self.busy = True
            self.sorted_indices.clear()

            sx1, sy1, _, _ = self.card_positions[source]
            sx2, sy2, _, _ = self.card_positions[target]
            tx1, ty1, _, _ = slots[target]
            tx2, ty2, _, _ = slots[source]

            self.cards[source], self.cards[target] = self.cards[target], self.cards[source]
            self.card_items[source], self.card_items[target] = self.card_items[target], self.card_items[source]
            self.card_positions[source], self.card_positions[target] = (
                self.card_positions[target], self.card_positions[source]
            )

            def finish_manual_swap():
                self.busy = False
                self.draw_cards()

            self.animate_trajectories(
                [
                    (target, sx1, sy1, tx1, ty1, 0),
                    (source, sx2, sy2, tx2, ty2, 22)
                ],
                10,
                finish_manual_swap
            )
        else:
            self.busy = True
            sx, sy, _, _ = self.card_positions[source]
            tx, ty, _, _ = slots[source]

            def finish_snap():
                self.busy = False
                self.draw_cards()

            self.animate_trajectories([(source, sx, sy, tx, ty, 0)], 8, finish_snap)

    # ======================================
    # SORTING VISUALIZER ENGINE
    # ======================================

    def start_sort(self, name):
        if self.busy:
            return

        self.busy = True
        self.algorithm = name
        self.sorted_indices.clear()
        self.draw_cards()

        self.comparisons = 0
        self.movements = 0
        self.update_stats()
        self.start_time = time.perf_counter()

        algo_map = {
            "Bubble Sort": bubble_sort,
            "Selection Sort": selection_sort,
            "Insertion Sort": insertion_sort,
            "Quick Sort": quick_sort,
            "Merge Sort": merge_sort
        }
        self.sort_generator = algo_map[name](self.cards)

        self.status_label.config(text=f"Visualizing {name}...")
        self.animate_sort_step()

    def animate_sort_step(self):
        if not self.root.winfo_exists():
            return

        try:
            step = next(self.sort_generator)
        except StopIteration:
            self.finish_sort_visualization()
            return

        action = step["action"]
        self.cards = step["cards"]
        self.comparisons = step["comparisons"]
        self.movements = step["movements"]
        self.sorted_indices = step["sorted"]

        self.update_stats()
        elapsed_now = time.perf_counter() - self.start_time
        self.time_label.config(text=f"Time: {elapsed_now:.6f} s")
        self.status_label.config(text=step["status"])

        slots, _, _ = self.compute_layout()

        # ----------------------------------
        # 1. BUBBLE SORT COMPARE
        # ----------------------------------
        if action == "compare":
            i, j = step["indices"]
            self.refresh_sorted_styles(
                self.sorted_indices,
                {
                    i: (GOLD, "#FEF9E7", "CMP"),
                    j: (GOLD, "#FEF9E7", "CMP")
                }
            )
            x1, y1, _, _ = slots[i]
            x2, y2, _, _ = slots[j]

            self.animate_trajectories(
                [
                    (i, x1, y1, x1, y1, 14),
                    (j, x2, y2, x2, y2, 14)
                ],
                10,
                self.animate_sort_step
            )

        # ----------------------------------
        # 2. SWAP (BUBBLE, SELECTION & QUICK)
        # ----------------------------------
        elif action == "swap":
            i, j = step["indices"]
            self.raise_card_z(i)
            self.raise_card_z(j)
            self.refresh_sorted_styles(
                self.sorted_indices,
                {
                    i: (RED, "#FDEDEC", "SWAP"),
                    j: (RED, "#FDEDEC", "SWAP")
                }
            )

            sx1, sy1, _, _ = self.card_positions[i]
            sx2, sy2, _, _ = self.card_positions[j]
            tx1, ty1, _, _ = slots[j]
            tx2, ty2, _, _ = slots[i]

            def complete_swap():
                self.card_items[i], self.card_items[j] = self.card_items[j], self.card_items[i]
                self.card_positions[i], self.card_positions[j] = (
                    self.card_positions[j], self.card_positions[i]
                )
                self.refresh_sorted_styles(self.sorted_indices)
                self.animate_sort_step()

            self.animate_trajectories(
                [
                    (i, sx1, sy1, tx1, ty1, 34),
                    (j, sx2, sy2, tx2, ty2, -34)
                ],
                16,
                complete_swap
            )

        # ----------------------------------
        # 3. SELECTION SORT SCAN & MINIMUM
        # ----------------------------------
        elif action == "select_min":
            min_idx = step["min_idx"]
            old_min = step["old_min"]
            self.raise_card_z(min_idx)

            self.refresh_sorted_styles(
                self.sorted_indices,
                {min_idx: (CYAN, "#EBF5FB", "MIN")}
            )

            traj = []
            mx, my, _, _ = self.card_positions[min_idx]
            slot_mx, slot_my, _, _ = slots[min_idx]
            traj.append((min_idx, mx, my, slot_mx, slot_my - 20, 0))

            if old_min is not None:
                ox, oy, _, _ = self.card_positions[old_min]
                slot_ox, slot_oy, _, _ = slots[old_min]
                traj.append((old_min, ox, oy, slot_ox, slot_oy, 0))

            self.animate_trajectories(traj, 9, self.animate_sort_step)

        elif action == "scan":
            scan_idx = step["scan_idx"]
            min_idx = step["min_idx"]
            self.refresh_sorted_styles(
                self.sorted_indices,
                {
                    min_idx: (CYAN, "#EBF5FB", "MIN"),
                    scan_idx: (GOLD, "#FEF9E7", "SCAN")
                }
            )
            sx, sy, _, _ = slots[scan_idx]
            self.animate_trajectories(
                [(scan_idx, sx, sy, sx, sy, 14)],
                8,
                self.animate_sort_step
            )

        elif action == "lower_min":
            min_idx = step["min_idx"]
            mx, my, _, _ = self.card_positions[min_idx]
            tx, ty, _, _ = slots[min_idx]

            def after_lower():
                self.refresh_sorted_styles(self.sorted_indices)
                self.animate_sort_step()

            self.animate_trajectories(
                [(min_idx, mx, my, tx, ty, 0)],
                8,
                after_lower
            )

        # ----------------------------------
        # 4. INSERTION SORT LIFT / SHIFT / DROP
        # ----------------------------------
        elif action == "lift_key":
            key_idx = step["key_idx"]
            self.raise_card_z(key_idx)
            self.refresh_sorted_styles(
                self.sorted_indices,
                {key_idx: (PURPLE, "#F5EEF8", "KEY")}
            )
            kx, ky, _, _ = self.card_positions[key_idx]
            tx, ty, _, _ = slots[key_idx]
            self.animate_trajectories(
                [(key_idx, kx, ky, tx, ty - 48, 0)],
                10,
                self.animate_sort_step
            )

        elif action == "compare_key":
            comp_idx = step["compare_idx"]
            key_idx = step["key_idx"]
            self.refresh_sorted_styles(
                self.sorted_indices,
                {
                    key_idx: (PURPLE, "#F5EEF8", "KEY"),
                    comp_idx: (GOLD, "#FEF9E7", "CMP")
                }
            )
            cx, cy, _, _ = slots[comp_idx]
            self.animate_trajectories(
                [(comp_idx, cx, cy, cx, cy, 12)],
                8,
                self.animate_sort_step
            )

        elif action == "shift_right":
            from_idx = step["from_idx"]
            to_idx = step["to_idx"]
            self.raise_card_z(to_idx)

            self.refresh_sorted_styles(
                self.sorted_indices,
                {
                    to_idx: (PURPLE, "#F5EEF8", "KEY"),
                    from_idx: (RED, "#FDEDEC", "SHIFT →")
                }
            )

            fx, fy, _, _ = self.card_positions[from_idx]
            kx, ky, _, _ = self.card_positions[to_idx]
            target_right_x, target_right_y, _, _ = slots[to_idx]
            target_left_x, _, _, _ = slots[from_idx]

            def complete_shift():
                self.card_items[from_idx], self.card_items[to_idx] = (
                    self.card_items[to_idx], self.card_items[from_idx]
                )
                self.card_positions[from_idx], self.card_positions[to_idx] = (
                    self.card_positions[to_idx], self.card_positions[from_idx]
                )
                self.animate_sort_step()

            self.animate_trajectories(
                [
                    (from_idx, fx, fy, target_right_x, target_right_y, 0),
                    (to_idx, kx, ky, target_left_x, ky, 0)
                ],
                12,
                complete_shift
            )

        elif action == "drop_key":
            key_idx = step["key_idx"]
            kx, ky, _, _ = self.card_positions[key_idx]
            tx, ty, _, _ = slots[key_idx]

            def after_drop():
                self.refresh_sorted_styles(self.sorted_indices)
                self.animate_sort_step()

            self.animate_trajectories(
                [(key_idx, kx, ky, tx, ty, 0)],
                10,
                after_drop
            )

        # ----------------------------------
        # 5. QUICK SORT PIVOT & PARTITION
        # ----------------------------------
        elif action == "mark_sorted":
            idx = step["index"]
            self.refresh_sorted_styles(self.sorted_indices)
            sx, sy, _, _ = slots[idx]
            self.animate_trajectories(
                [(idx, sx, sy, sx, sy, 14)],
                6,
                self.animate_sort_step
            )

        elif action == "pivot_lift":
            pivot_idx = step["pivot_idx"]
            self.raise_card_z(pivot_idx)
            self.refresh_sorted_styles(
                self.sorted_indices,
                {pivot_idx: (PINK, "#FDEDEC", "PIVOT")}
            )
            px, py, _, _ = self.card_positions[pivot_idx]
            tx, ty, _, _ = slots[pivot_idx]
            self.animate_trajectories(
                [(pivot_idx, px, py, tx, ty - 28, 0)],
                10,
                self.animate_sort_step
            )

        elif action == "pivot_compare":
            scan_idx = step["scan_idx"]
            pivot_idx = step["pivot_idx"]
            bound_idx = step["bound_idx"]

            badges = {
                pivot_idx: (PINK, "#FDEDEC", "PIVOT"),
                scan_idx: (GOLD, "#FEF9E7", "SCAN")
            }
            if bound_idx is not None and bound_idx != scan_idx:
                badges[bound_idx] = (ORANGE, "#FEF5E7", "BOUND")

            self.refresh_sorted_styles(self.sorted_indices, badges)
            sx, sy, _, _ = slots[scan_idx]
            self.animate_trajectories(
                [(scan_idx, sx, sy, sx, sy, 14)],
                8,
                self.animate_sort_step
            )

        elif action == "pivot_swap":
            i, j = step["indices"]
            pivot_idx = step["pivot_idx"]
            self.raise_card_z(i)
            self.raise_card_z(j)

            self.refresh_sorted_styles(
                self.sorted_indices,
                {
                    pivot_idx: (PINK, "#FDEDEC", "PIVOT"),
                    i: (RED, "#FDEDEC", "SWAP"),
                    j: (RED, "#FDEDEC", "SWAP")
                }
            )

            sx1, sy1, _, _ = self.card_positions[i]
            sx2, sy2, _, _ = self.card_positions[j]
            tx1, ty1, _, _ = slots[j]
            tx2, ty2, _, _ = slots[i]

            def complete_pivot_swap():
                self.card_items[i], self.card_items[j] = self.card_items[j], self.card_items[i]
                self.card_positions[i], self.card_positions[j] = (
                    self.card_positions[j], self.card_positions[i]
                )
                self.animate_sort_step()

            self.animate_trajectories(
                [
                    (i, sx1, sy1, tx1, ty1, 32),
                    (j, sx2, sy2, tx2, ty2, -32)
                ],
                14,
                complete_pivot_swap
            )

        # ----------------------------------
        # 6. MERGE SORT 2-LANE BUFFER MERGE
        # ----------------------------------
        elif action == "merge_lift":
            left = step["left"]
            mid = step["mid"]
            right = step["right"]

            badges = self.build_merge_badges(left, mid, right, set())
            self.refresh_sorted_styles(self.sorted_indices, badges)

            traj = []
            for idx in range(left, right + 1):
                self.raise_card_z(idx)
                sx, sy, _, _ = self.card_positions[idx]
                tx, ty, _, _ = slots[idx]
                traj.append((idx, sx, sy, tx, ty - 56, 0))

            self.animate_trajectories(traj, 12, self.animate_sort_step)

        elif action == "merge_compare":
            l_idx = step["l_idx"]
            r_idx = step["r_idx"]
            left = step["left"]
            mid = step["mid"]
            right = step["right"]
            dropped = step["dropped"]

            badges = self.build_merge_badges(
                left, mid, right, dropped,
                {
                    l_idx: (GOLD, "#FEF9E7", "CMP"),
                    r_idx: (GOLD, "#FEF9E7", "CMP")
                }
            )
            self.refresh_sorted_styles(self.sorted_indices, badges)

            lx, ly, _, _ = self.card_positions[l_idx]
            rx, ry, _, _ = self.card_positions[r_idx]
            self.animate_trajectories(
                [
                    (l_idx, lx, ly, lx, ly, 10),
                    (r_idx, rx, ry, rx, ry, 10)
                ],
                8,
                self.animate_sort_step
            )

        elif action == "merge_drop":
            from_idx = step["from_idx"]
            to_slot = step["to_slot"]
            left = step["left"]
            mid = step["mid"]
            right = step["right"]
            dropped = step["dropped"]

            self.raise_card_z(from_idx)
            badges = self.build_merge_badges(
                left, mid, right, dropped,
                {from_idx: (BRIGHT_GREEN, "#EAFAF1", "MERGE ↓")}
            )
            self.refresh_sorted_styles(self.sorted_indices, badges)

            sx, sy, _, _ = self.card_positions[from_idx]
            tx, ty, _, _ = slots[to_slot]
            self.animate_trajectories(
                [(from_idx, sx, sy, tx, ty, 10)],
                12,
                self.animate_sort_step
            )

        elif action == "merge_commit":
            left = step["left"]
            right = step["right"]
            order = step["order"]

            # Rebind canvas items & positions to their newly merged slot order
            self.card_items[left:right + 1] = [self.card_items[i] for i in order]
            self.card_positions[left:right + 1] = [self.card_positions[i] for i in order]
            self.refresh_sorted_styles(self.sorted_indices)
            self.root.after(20, self.animate_sort_step)

        # ----------------------------------
        # 7. SORT COMPLETED
        # ----------------------------------
        elif action == "done":
            self.refresh_sorted_styles(self.sorted_indices)
            self.finish_sort_visualization()

    def finish_sort_visualization(self):
        elapsed = time.perf_counter() - self.start_time
        self.time_label.config(text=f"Time: {elapsed:.6f} s")
        self.status_label.config(text=f"✅ {self.algorithm} completed!")

        def after_wave():
            self.busy = False
            messagebox.showinfo(
                "Sorting Completed",
                f"Algorithm: {self.algorithm}\n\n"
                f"Comparisons: {self.comparisons}\n"
                f"Swaps/Shifts: {self.movements}\n"
                f"Visualized time: {elapsed:.6f} seconds"
            )

        self.celebrate_wave(on_done=after_wave)

    # ======================================
    # STATISTICS
    # ======================================

    def update_stats(self):
        self.comparison_label.config(text=f"Comparisons: {self.comparisons}")
        self.movement_label.config(text=f"Swaps/Shifts: {self.movements}")

    # ======================================
    # ALGORITHM COMPARISON
    # ======================================

    def compare_algorithms(self):
        if self.busy:
            return

        test_cards = random.sample(create_deck(), 12)

        algorithms = [
            ("Bubble Sort", bubble_sort),
            ("Selection Sort", selection_sort),
            ("Insertion Sort", insertion_sort),
            ("Quick Sort", quick_sort),
            ("Merge Sort", merge_sort)
        ]

        results = []

        for name, algorithm in algorithms:
            start = time.perf_counter()

            final_state = None
            comparisons = 0
            movements = 0

            for step in algorithm(test_cards):
                final_state = step["cards"]
                comparisons = step["comparisons"]
                movements = step["movements"]

            elapsed = time.perf_counter() - start

            if final_state is None:
                final_state = test_cards.copy()

            results.append((name, comparisons, movements, elapsed, final_state))

        window = tk.Toplevel(self.root)
        window.title("Algorithm Performance")
        window.geometry("740x480")
        window.configure(bg=BG)

        tk.Label(
            window,
            text="📊 ALGORITHM PERFORMANCE COMPARISON",
            font=("Arial", 17, "bold"),
            bg=BG,
            fg=GOLD
        ).pack(pady=16)

        tk.Label(
            window,
            text="Test data: 12 randomly selected playing cards (identical starting order)",
            font=("Arial", 10),
            bg=BG,
            fg=MUTED
        ).pack(pady=4)

        table = tk.Frame(window, bg=PANEL)
        table.pack(fill="x", padx=25, pady=15)

        headers = ["Algorithm", "Comparisons", "Movements", "Time (seconds)"]

        for col, header in enumerate(headers):
            table.grid_columnconfigure(col, weight=1)
            tk.Label(
                table,
                text=header,
                font=("Arial", 10, "bold"),
                bg=PANEL,
                fg=GOLD,
                padx=7,
                pady=10
            ).grid(row=0, column=col)

        for row, result in enumerate(results, start=1):
            name, comparisons, movements, elapsed, _ = result
            values = [name, comparisons, movements, f"{elapsed:.8f}"]

            for col, value in enumerate(values):
                tk.Label(
                    table,
                    text=str(value),
                    font=("Arial", 10),
                    bg=PANEL,
                    fg=WHITE,
                    padx=7,
                    pady=9
                ).grid(row=row, column=col)

        tk.Label(
            window,
            text=(
                "Divide-and-Conquer algorithms (Quick Sort & Merge Sort) scale in O(n log n) time,\n"
                "while Bubble, Selection, and Insertion Sort scale in O(n²) average/worst-case time."
            ),
            font=("Arial", 10),
            bg=BG,
            fg=MUTED
        ).pack(pady=8)

        tk.Button(
            window,
            text="Close",
            command=window.destroy,
            bg=GREEN,
            fg=WHITE,
            font=("Arial", 10, "bold"),
            activebackground=GOLD,
            activeforeground=BG,
            relief="flat",
            padx=16,
            pady=6,
            cursor="hand2"
        ).pack(pady=10)


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":
    root = tk.Tk()
    app = CardSortingGame(root)
    root.mainloop()