
# --- Heatmap of ACCD & related enzyme scores (all rows and columns visible) ---

# Install required packages if not already installed
if (!require("pheatmap")) install.packages("pheatmap")
if (!require("readr")) install.packages("readr")

library(pheatmap)
library(readr)

# 1) Load the data
data <- read_csv("C:/Users/manikrow/OneDrive - University of Manitoba/Desktop/Raveena_Projects/BENEFIT Activity 1.1/PromethION/2.sub_analysis/nifH_genes/nifH_presence_absence_by_type_allgenomes.csv") 
# Convert tibble -> data.frame before setting row names
data_df <- as.data.frame(data, check.names = FALSE, stringsAsFactors = FALSE)
stopifnot("genome" %in% colnames(data_df))
rownames(data_df) <- data_df$genome

# Keep all columns except 'genome'
score_df <- data_df[, setdiff(colnames(data_df), "genome")]

# Make sure columns are numeric but preserve row names
score_df[] <- lapply(score_df, function(x) {
  if (is.numeric(x)) x else suppressWarnings(as.numeric(x))
})

# Convert to matrix (ROW NAMES PRESERVED)
mat <- as.matrix(score_df)

# Optional: handle NA
if (any(is.na(mat))) mat[is.na(mat)] <- 0


# --- Save a VERY TALL heatmap in pixel units ---

nr <- nrow(mat); nc <- ncol(mat)

# Tune these for readability
cellheight <- 14  # px per row (increase to make row labels bigger)
cellwidth  <- 30  # px per col (increase if column labels are long)
# Padding (pixels) for title, legend, dendrograms, margins
pad_top    <- 200    # title
pad_bottom <- 120   # legend/color key
pad_left   <- 200    # left margin
pad_right  <-120    # right margin
tree_row   <- 80    # row dendrogram height
tree_col   <- 80    # column dendrogram height

# Final canvas size (pixels)
height_px <- nr * cellheight + tree_row + pad_top + pad_bottom
width_px  <- nc * cellwidth  + tree_col + pad_left + pad_right

out_file <- ("C:/Users/manikrow/OneDrive - University of Manitoba/Desktop/Raveena_Projects/BENEFIT Activity 1.1/PromethION/2.sub_analysis/nifH_genes/nifH_presence_absence_by_type_allgenomes.png")

# Open PNG in pixel units (no DPI computation needed)
png(filename = out_file, width = width_px, height = height_px, units = "px")

pheatmap(
  mat,
  cluster_rows = TRUE, cluster_cols = TRUE,
  show_rownames = TRUE, show_colnames = TRUE,
  labels_row = rownames(mat),
  color = colorRampPalette(c("white","skyblue","royalblue","navy"))(200),
  main = "Heatmap of ACCD & Related Enzyme Scores",
  border_color = "grey",
  fontsize_row = 10,   # label font; tweak with cellheight
  fontsize_col = 10,
  cellheight = cellheight,
  cellwidth  = cellwidth,
  treeheight_row = tree_row,
  treeheight_col = tree_col
)

dev.off()

cat(sprintf("Saved heatmap./nRows: %d, Cols: %d/nSize: %d x %d px\nCell: %d x %d px\n",
  nr, nc, width_px, height_px, cellwidth, cellheight))
  
  