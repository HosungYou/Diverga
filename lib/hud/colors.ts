/**
 * Diverga HUD - ANSI Color Utilities
 *
 * Provides ANSI escape codes for terminal color formatting.
 * Used by the HUD statusline renderer.
 *
 * @module lib/hud/colors
 * @version 8.0.0
 */

// ANSI escape codes
const ESC = '\x1b[';

// Reset
export const RESET = `${ESC}0m`;

// Basic colors (foreground)
export const BLACK = `${ESC}30m`;
export const RED = `${ESC}31m`;
export const GREEN = `${ESC}32m`;
export const YELLOW = `${ESC}33m`;
export const BLUE = `${ESC}34m`;
export const MAGENTA = `${ESC}35m`;
export const CYAN = `${ESC}36m`;
export const WHITE = `${ESC}37m`;

// Bright colors (foreground)
export const BRIGHT_BLACK = `${ESC}90m`;
export const BRIGHT_RED = `${ESC}91m`;
export const BRIGHT_GREEN = `${ESC}92m`;
export const BRIGHT_YELLOW = `${ESC}93m`;
export const BRIGHT_BLUE = `${ESC}94m`;
export const BRIGHT_MAGENTA = `${ESC}95m`;
export const BRIGHT_CYAN = `${ESC}96m`;
export const BRIGHT_WHITE = `${ESC}97m`;

// Background colors
export const BG_BLACK = `${ESC}40m`;
export const BG_RED = `${ESC}41m`;
export const BG_GREEN = `${ESC}42m`;
export const BG_YELLOW = `${ESC}43m`;
export const BG_BLUE = `${ESC}44m`;
export const BG_MAGENTA = `${ESC}45m`;
export const BG_CYAN = `${ESC}46m`;
export const BG_WHITE = `${ESC}47m`;

// Styles
export const BOLD = `${ESC}1m`;
export const DIM = `${ESC}2m`;
export const ITALIC = `${ESC}3m`;
export const UNDERLINE = `${ESC}4m`;

/**
 * Color a string with the specified color code
 */
export function color(text: string, colorCode: string): string {
  return `${colorCode}${text}${RESET}`;
}

/**
 * Make text bold
 */
export function bold(text: string): string {
  return `${BOLD}${text}${RESET}`;
}

/**
 * Make text dim
 */
export function dim(text: string): string {
  return `${DIM}${text}${RESET}`;
}

/**
 * Combine multiple styles
 */
export function styled(text: string, ...styles: string[]): string {
  return `${styles.join('')}${text}${RESET}`;
}

// Semantic colors for HUD
export const HUD_COLORS = {
  // Status indicators
  success: GREEN,
  warning: YELLOW,
  error: RED,
  info: CYAN,

  // Progress bar
  filled: BRIGHT_GREEN,
  empty: DIM,

  // Stage colors
  active: BRIGHT_CYAN,
  completed: GREEN,
  pending: DIM,

  // Memory health
  healthy: GREEN,
  moderate: YELLOW,
  critical: RED,

  // Labels
  label: BRIGHT_WHITE,
  value: WHITE,
  separator: DIM,

  // Icons
  icon: BRIGHT_MAGENTA,
};

/**
 * Get memory health color based on percentage
 */
export function memoryHealthColor(percent: number): string {
  if (percent >= 70) return HUD_COLORS.healthy;
  if (percent >= 40) return HUD_COLORS.moderate;
  return HUD_COLORS.critical;
}

/**
 * Get checkpoint status color
 */
export function checkpointColor(status: 'completed' | 'pending' | 'active'): string {
  switch (status) {
    case 'completed': return HUD_COLORS.completed;
    case 'active': return HUD_COLORS.active;
    default: return HUD_COLORS.pending;
  }
}

export default {
  RESET,
  BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE,
  BRIGHT_BLACK, BRIGHT_RED, BRIGHT_GREEN, BRIGHT_YELLOW, BRIGHT_BLUE, BRIGHT_MAGENTA, BRIGHT_CYAN, BRIGHT_WHITE,
  BG_BLACK, BG_RED, BG_GREEN, BG_YELLOW, BG_BLUE, BG_MAGENTA, BG_CYAN, BG_WHITE,
  BOLD, DIM, ITALIC, UNDERLINE,
  color, bold, dim, styled,
  HUD_COLORS, memoryHealthColor, checkpointColor
};
