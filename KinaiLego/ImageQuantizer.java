import javax.swing.*;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.awt.*;
import java.awt.event.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;
import java.awt.datatransfer.*;
import java.awt.dnd.*;
import java.util.List;

/**
 * Image Quantizer - Transform your image into 64×64 with 5 shades of gray
 * This application processes images by:
 * - Resizing to fit within 64×64 pixels (aspect ratio preserved)
 * - Converting to grayscale
 * - Quantizing to 5 perceptually uniform gray levels (0, 76, 128, 179, 255)
 */
public class ImageQuantizer extends JFrame {
    // The 5 shades of gray - perceptually uniform (gamma corrected)
    private static final int[] GRAY_LEVELS = {0, 76, 128, 179, 255};
    
    private BufferedImage originalImage;
    private BufferedImage quantizedImage;
    private Color backgroundColor = Color.WHITE;
    
    private JPanel originalPanel;
    private JPanel quantizedPanel;
    private JPanel comparisonPanel;
    private ComparisonSliderPanel sliderPanel;
    private JButton uploadButton;
    private JButton colorButton;
    private JLabel statusLabel;
    
    public ImageQuantizer() {
        setTitle("Image Quantizer - 5 Shades of Gray");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout(10, 10));
        
        initComponents();
        
        setSize(1000, 800);
        setLocationRelativeTo(null);
        setVisible(true);
    }
    
    private void initComponents() {
        // Header Panel
        JPanel headerPanel = new JPanel(new BorderLayout());
        headerPanel.setBackground(new Color(102, 126, 234));
        headerPanel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
        
        JLabel titleLabel = new JLabel("🎨 Image Quantizer", SwingConstants.CENTER);
        titleLabel.setFont(new Font("Segoe UI", Font.BOLD, 32));
        titleLabel.setForeground(Color.WHITE);
        
        JLabel subtitleLabel = new JLabel("Transform your image into 64×64 with 5 shades of gray", SwingConstants.CENTER);
        subtitleLabel.setFont(new Font("Segoe UI", Font.PLAIN, 14));
        subtitleLabel.setForeground(Color.WHITE);
        
        JPanel titleContainer = new JPanel(new GridLayout(2, 1, 0, 5));
        titleContainer.setOpaque(false);
        titleContainer.add(titleLabel);
        titleContainer.add(subtitleLabel);
        
        headerPanel.add(titleContainer, BorderLayout.CENTER);
        add(headerPanel, BorderLayout.NORTH);
        
        // Control Panel
        JPanel controlPanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 15, 10));
        controlPanel.setBackground(Color.WHITE);
        
        uploadButton = new JButton("📂 Upload Image");
        uploadButton.setFont(new Font("Segoe UI", Font.BOLD, 14));
        uploadButton.setBackground(new Color(102, 126, 234));
        uploadButton.setForeground(Color.WHITE);
        uploadButton.setFocusPainted(false);
        uploadButton.setBorderPainted(false);
        uploadButton.setPreferredSize(new Dimension(160, 40));
        uploadButton.setCursor(new Cursor(Cursor.HAND_CURSOR));
        uploadButton.addActionListener(e -> uploadImage());
        
        colorButton = new JButton("🎨 Background Color");
        colorButton.setFont(new Font("Segoe UI", Font.BOLD, 14));
        colorButton.setBackground(new Color(118, 75, 162));
        colorButton.setForeground(Color.WHITE);
        colorButton.setFocusPainted(false);
        colorButton.setBorderPainted(false);
        colorButton.setPreferredSize(new Dimension(180, 40));
        colorButton.setCursor(new Cursor(Cursor.HAND_CURSOR));
        colorButton.addActionListener(e -> selectBackgroundColor());
        
        statusLabel = new JLabel("Upload an image to begin");
        statusLabel.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        statusLabel.setForeground(Color.GRAY);
        
        controlPanel.add(uploadButton);
        controlPanel.add(colorButton);
        controlPanel.add(statusLabel);
        add(controlPanel, BorderLayout.SOUTH);
        
        // Center Panel with tabs
        JTabbedPane tabbedPane = new JTabbedPane();
        tabbedPane.setFont(new Font("Segoe UI", Font.BOLD, 12));
        
        // Original and Quantized side-by-side panel
        JPanel imagesPanel = new JPanel(new GridLayout(1, 2, 10, 10));
        imagesPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        imagesPanel.setBackground(Color.WHITE);
        
        originalPanel = createImagePanel("Original Image");
        quantizedPanel = createImagePanel("Quantized (64×64, 5 Grays)");
        
        imagesPanel.add(originalPanel);
        imagesPanel.add(quantizedPanel);
        
        // Comparison panel
        JPanel comparisonContainer = new JPanel(new BorderLayout());
        comparisonContainer.setBackground(Color.WHITE);
        comparisonContainer.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
        
        JLabel comparisonTitle = new JLabel("Before/After Comparison - Drag the slider", SwingConstants.CENTER);
        comparisonTitle.setFont(new Font("Segoe UI", Font.BOLD, 16));
        comparisonTitle.setBorder(BorderFactory.createEmptyBorder(0, 0, 15, 0));
        
        sliderPanel = new ComparisonSliderPanel();
        
        comparisonContainer.add(comparisonTitle, BorderLayout.NORTH);
        comparisonContainer.add(sliderPanel, BorderLayout.CENTER);
        
        // Info Panel
        JPanel infoPanel = new JPanel();
        infoPanel.setLayout(new BoxLayout(infoPanel, BoxLayout.Y_AXIS));
        infoPanel.setBackground(Color.WHITE);
        infoPanel.setBorder(BorderFactory.createEmptyBorder(20, 40, 20, 40));
        
        addInfoText(infoPanel, "How it works:", true);
        addInfoText(infoPanel, "• Upload any image (JPG, PNG, etc.) using the button or drag-and-drop", false);
        addInfoText(infoPanel, "• The image will be resized to fit within 64×64 pixels (aspect ratio preserved)", false);
        addInfoText(infoPanel, "• Choose background color for letterboxing (default: white)", false);
        addInfoText(infoPanel, "• Colors will be converted to 5 perceptually uniform shades of gray", false);
        addInfoText(infoPanel, "• Gamma-corrected for natural visual perception", false);
        
        infoPanel.add(Box.createVerticalStrut(20));
        addInfoText(infoPanel, "Quantization Palette:", true);
        
        JPanel palettePanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 10, 10));
        palettePanel.setOpaque(false);
        for (int level : GRAY_LEVELS) {
            palettePanel.add(createPaletteSwatch(level));
        }
        infoPanel.add(palettePanel);
        
        tabbedPane.addTab("📊 Images", imagesPanel);
        tabbedPane.addTab("⚖️ Comparison", comparisonContainer);
        tabbedPane.addTab("ℹ️ Info", new JScrollPane(infoPanel));
        
        add(tabbedPane, BorderLayout.CENTER);
        
        // Setup drag and drop
        setupDragAndDrop();
    }
    
    private void addInfoText(JPanel panel, String text, boolean bold) {
        JLabel label = new JLabel(text);
        label.setFont(new Font("Segoe UI", bold ? Font.BOLD : Font.PLAIN, 13));
        label.setBorder(BorderFactory.createEmptyBorder(3, 0, 3, 0));
        label.setAlignmentX(Component.LEFT_ALIGNMENT);
        panel.add(label);
    }
    
    private JPanel createPaletteSwatch(int grayValue) {
        JPanel swatch = new JPanel(new BorderLayout());
        swatch.setPreferredSize(new Dimension(60, 60));
        swatch.setBackground(new Color(grayValue, grayValue, grayValue));
        swatch.setBorder(BorderFactory.createLineBorder(Color.BLACK, 2));
        
        JLabel label = new JLabel(String.valueOf(grayValue), SwingConstants.CENTER);
        label.setFont(new Font("Segoe UI", Font.BOLD, 11));
        label.setForeground(grayValue < 128 ? Color.WHITE : Color.BLACK);
        swatch.add(label);
        
        return swatch;
    }
    
    private JPanel createImagePanel(String title) {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBackground(Color.WHITE);
        panel.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(new Color(200, 200, 200), 1),
            BorderFactory.createEmptyBorder(10, 10, 10, 10)
        ));
        
        JLabel titleLabel = new JLabel(title, SwingConstants.CENTER);
        titleLabel.setFont(new Font("Segoe UI", Font.BOLD, 14));
        titleLabel.setBorder(BorderFactory.createEmptyBorder(0, 0, 10, 0));
        
        JLabel imageLabel = new JLabel("No image", SwingConstants.CENTER);
        imageLabel.setPreferredSize(new Dimension(320, 320));
        imageLabel.setOpaque(true);
        imageLabel.setBackground(new Color(248, 249, 250));
        imageLabel.setBorder(BorderFactory.createLineBorder(new Color(200, 200, 200), 2));
        
        panel.add(titleLabel, BorderLayout.NORTH);
        panel.add(imageLabel, BorderLayout.CENTER);
        
        return panel;
    }
    
    private void setupDragAndDrop() {
        new DropTarget(this, new DropTargetAdapter() {
            @Override
            public void drop(DropTargetDropEvent dtde) {
                try {
                    dtde.acceptDrop(DnDConstants.ACTION_COPY);
                    Transferable transferable = dtde.getTransferable();
                    
                    if (transferable.isDataFlavorSupported(DataFlavor.javaFileListFlavor)) {
                        @SuppressWarnings("unchecked")
                        List<File> files = (List<File>) transferable.getTransferData(DataFlavor.javaFileListFlavor);
                        if (!files.isEmpty()) {
                            File file = files.get(0);
                            if (isImageFile(file)) {
                                loadImage(file);
                            } else {
                                JOptionPane.showMessageDialog(ImageQuantizer.this, 
                                    "Please drop an image file (JPG, PNG, etc.)", 
                                    "Invalid File", JOptionPane.WARNING_MESSAGE);
                            }
                        }
                    }
                    dtde.dropComplete(true);
                } catch (Exception e) {
                    e.printStackTrace();
                    dtde.dropComplete(false);
                }
            }
        });
    }
    
    private boolean isImageFile(File file) {
        String name = file.getName().toLowerCase();
        return name.endsWith(".jpg") || name.endsWith(".jpeg") || 
               name.endsWith(".png") || name.endsWith(".gif") || 
               name.endsWith(".bmp");
    }
    
    private void uploadImage() {
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setFileFilter(new FileNameExtensionFilter(
            "Image Files", "jpg", "jpeg", "png", "gif", "bmp"));
        
        int result = fileChooser.showOpenDialog(this);
        if (result == JFileChooser.APPROVE_OPTION) {
            File selectedFile = fileChooser.getSelectedFile();
            loadImage(selectedFile);
        }
    }
    
    private void selectBackgroundColor() {
        Color newColor = JColorChooser.showDialog(this, "Select Background Color", backgroundColor);
        if (newColor != null) {
            backgroundColor = newColor;
            if (originalImage != null) {
                processImage(originalImage);
            }
        }
    }
    
    private void loadImage(File file) {
        try {
            BufferedImage img = ImageIO.read(file);
            if (img == null) {
                throw new IOException("Unable to read image file");
            }
            originalImage = img;
            statusLabel.setText("Image loaded: " + file.getName());
            processImage(img);
        } catch (IOException e) {
            JOptionPane.showMessageDialog(this, 
                "Error loading image: " + e.getMessage(), 
                "Error", JOptionPane.ERROR_MESSAGE);
        }
    }
    
    private void processImage(BufferedImage img) {
        // Create display version (320x320) of original
        BufferedImage displayOriginal = createDisplayImage(img, 320, backgroundColor);
        updateImagePanel(originalPanel, displayOriginal);
        
        // Create 64x64 quantized version
        BufferedImage temp64 = createDisplayImage(img, 64, backgroundColor);
        quantizedImage = quantizeImage(temp64);
        
        // Scale up to 320x320 for display
        BufferedImage displayQuantized = scaleImage(quantizedImage, 320, false);
        updateImagePanel(quantizedPanel, displayQuantized);
        
        // Update comparison panel
        sliderPanel.setImages(displayOriginal, displayQuantized);
        
        statusLabel.setText("Processing complete ✓");
    }
    
    private BufferedImage createDisplayImage(BufferedImage img, int maxSize, Color bgColor) {
        BufferedImage result = new BufferedImage(maxSize, maxSize, BufferedImage.TYPE_INT_RGB);
        Graphics2D g2d = result.createGraphics();
        
        // Fill with background color
        g2d.setColor(bgColor);
        g2d.fillRect(0, 0, maxSize, maxSize);
        
        // Calculate dimensions to maintain aspect ratio
        double scale = Math.min((double) maxSize / img.getWidth(), 
                                 (double) maxSize / img.getHeight());
        int width = (int) (img.getWidth() * scale);
        int height = (int) (img.getHeight() * scale);
        int x = (maxSize - width) / 2;
        int y = (maxSize - height) / 2;
        
        // Draw centered image
        g2d.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BILINEAR);
        g2d.drawImage(img, x, y, width, height, null);
        g2d.dispose();
        
        return result;
    }
    
    private BufferedImage scaleImage(BufferedImage img, int size, boolean smooth) {
        BufferedImage result = new BufferedImage(size, size, BufferedImage.TYPE_INT_RGB);
        Graphics2D g2d = result.createGraphics();
        
        if (smooth) {
            g2d.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BILINEAR);
        } else {
            g2d.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_NEAREST_NEIGHBOR);
        }
        
        g2d.drawImage(img, 0, 0, size, size, null);
        g2d.dispose();
        
        return result;
    }
    
    private BufferedImage quantizeImage(BufferedImage img) {
        BufferedImage result = new BufferedImage(img.getWidth(), img.getHeight(), BufferedImage.TYPE_INT_RGB);
        
        for (int y = 0; y < img.getHeight(); y++) {
            for (int x = 0; x < img.getWidth(); x++) {
                int rgb = img.getRGB(x, y);
                
                // Extract RGB components
                int r = (rgb >> 16) & 0xFF;
                int g = (rgb >> 8) & 0xFF;
                int b = rgb & 0xFF;
                
                // Convert to grayscale using luminosity method
                int gray = (int) (0.299 * r + 0.587 * g + 0.114 * b);
                
                // Quantize to nearest gray level
                int quantized = findNearestGrayLevel(gray);
                
                // Create RGB value from quantized gray
                int newRgb = (quantized << 16) | (quantized << 8) | quantized;
                result.setRGB(x, y, newRgb);
            }
        }
        
        return result;
    }
    
    private int findNearestGrayLevel(int value) {
        int nearest = GRAY_LEVELS[0];
        int minDiff = Math.abs(value - GRAY_LEVELS[0]);
        
        for (int i = 1; i < GRAY_LEVELS.length; i++) {
            int diff = Math.abs(value - GRAY_LEVELS[i]);
            if (diff < minDiff) {
                minDiff = diff;
                nearest = GRAY_LEVELS[i];
            }
        }
        
        return nearest;
    }
    
    private void updateImagePanel(JPanel panel, BufferedImage image) {
        JLabel imageLabel = (JLabel) ((BorderLayout) panel.getLayout()).getLayoutComponent(BorderLayout.CENTER);
        if (imageLabel != null) {
            imageLabel.setIcon(new ImageIcon(image));
            imageLabel.setText("");
        }
    }
    
    // Inner class for comparison slider
    class ComparisonSliderPanel extends JPanel {
        private BufferedImage originalImg;
        private BufferedImage quantizedImg;
        private int sliderX = 160;
        private boolean dragging = false;
        
        public ComparisonSliderPanel() {
            setPreferredSize(new Dimension(320, 340));
            setBackground(Color.WHITE);
            
            MouseAdapter mouseAdapter = new MouseAdapter() {
                @Override
                public void mousePressed(MouseEvent e) {
                    if (originalImg != null) {
                        dragging = true;
                        updateSlider(e.getX());
                    }
                }
                
                @Override
                public void mouseReleased(MouseEvent e) {
                    dragging = false;
                }
                
                @Override
                public void mouseDragged(MouseEvent e) {
                    if (dragging && originalImg != null) {
                        updateSlider(e.getX());
                    }
                }
            };
            
            addMouseListener(mouseAdapter);
            addMouseMotionListener(mouseAdapter);
            setCursor(new Cursor(Cursor.E_RESIZE_CURSOR));
        }
        
        private void updateSlider(int x) {
            sliderX = Math.max(0, Math.min(x, 320));
            repaint();
        }
        
        public void setImages(BufferedImage original, BufferedImage quantized) {
            this.originalImg = original;
            this.quantizedImg = quantized;
            sliderX = 160;
            repaint();
        }
        
        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            Graphics2D g2d = (Graphics2D) g;
            
            if (originalImg == null || quantizedImg == null) {
                g2d.setColor(Color.GRAY);
                g2d.setFont(new Font("Segoe UI", Font.PLAIN, 14));
                String msg = "No image loaded";
                FontMetrics fm = g2d.getFontMetrics();
                int x = (getWidth() - fm.stringWidth(msg)) / 2;
                int y = getHeight() / 2;
                g2d.drawString(msg, x, y);
                return;
            }
            
            int offsetX = (getWidth() - 320) / 2;
            int offsetY = (getHeight() - 320) / 2;
            
            // Draw quantized (full)
            g2d.drawImage(quantizedImg, offsetX, offsetY, null);
            
            // Draw original (clipped)
            g2d.setClip(offsetX, offsetY, sliderX, 320);
            g2d.drawImage(originalImg, offsetX, offsetY, null);
            g2d.setClip(null);
            
            // Draw slider
            g2d.setColor(new Color(102, 126, 234));
            g2d.fillRect(offsetX + sliderX - 2, offsetY, 4, 320);
            
            // Draw slider handle
            g2d.setColor(new Color(102, 126, 234));
            g2d.fillOval(offsetX + sliderX - 12, offsetY + 160 - 12, 24, 24);
            g2d.setColor(Color.WHITE);
            g2d.setFont(new Font("Arial", Font.PLAIN, 10));
            g2d.drawString("◀▶", offsetX + sliderX - 10, offsetY + 160 + 4);
            
            // Draw border
            g2d.setColor(new Color(200, 200, 200));
            g2d.drawRect(offsetX, offsetY, 320, 320);
        }
    }
    
    public static void main(String[] args) {
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        SwingUtilities.invokeLater(() -> new ImageQuantizer());
    }
}
