import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.image.*;
import java.io.*;
import javax.imageio.ImageIO;

// ----- Lógica POO de imagen y filtros -----
class Imagen {
    BufferedImage imagen;
    String ruta;

    public void cargar(String ruta) throws IOException {
        this.ruta = ruta;
        this.imagen = ImageIO.read(new File(ruta));
    }

    public void guardar(String rutaDestino) throws IOException {
        if (imagen != null) {
            ImageIO.write(imagen, "jpg", new File(rutaDestino));
        }
    }
}

abstract class Filtro {
    public abstract void aplicar(Imagen imagen);
}

class FiltroGrises extends Filtro {
    @Override
    public void aplicar(Imagen imagen) {
        BufferedImage img = imagen.imagen;
        for (int y = 0; y < img.getHeight(); y++) {
            for (int x = 0; x < img.getWidth(); x++) {
                Color c = new Color(img.getRGB(x, y));
                int gris = (c.getRed() + c.getGreen() + c.getBlue()) / 3;
                Color nuevo = new Color(gris, gris, gris);
                img.setRGB(x, y, nuevo.getRGB());
            }
        }
    }
}

class FiltroInversion extends Filtro {
    @Override
    public void aplicar(Imagen imagen) {
        BufferedImage img = imagen.imagen;
        for (int y = 0; y < img.getHeight(); y++) {
            for (int x = 0; x < img.getWidth(); x++) {
                Color c = new Color(img.getRGB(x, y));
                Color invertido = new Color(255 - c.getRed(), 255 - c.getGreen(), 255 - c.getBlue());
                img.setRGB(x, y, invertido.getRGB());
            }
        }
    }
}

// ----- Interfaz Gráfica con Swing -----
public class EditorImagenApp extends JFrame {
    private Imagen imagen = new Imagen();
    private JLabel canvas = new JLabel();

    public EditorImagenApp() {
        setTitle("Editor de Imágenes - Filtros Básicos");
        setLayout(new FlowLayout());
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(500, 500);

        JButton btnCargar = new JButton("Cargar Imagen");
        JButton btnGrises = new JButton("Aplicar Filtro Grises");
        JButton btnInvertir = new JButton("Aplicar Filtro Inversión");
        JButton btnGuardar = new JButton("Guardar Imagen");

        btnCargar.addActionListener(e -> cargarImagen());
        btnGrises.addActionListener(e -> aplicarFiltro(new FiltroGrises()));
        btnInvertir.addActionListener(e -> aplicarFiltro(new FiltroInversion()));
        btnGuardar.addActionListener(e -> guardarImagen());

        add(btnCargar);
        add(btnGrises);
        add(btnInvertir);
        add(btnGuardar);
        add(canvas);

        setVisible(true);
    }

    private void mostrarImagen() {
        if (imagen.imagen != null) {
            ImageIcon icon = new ImageIcon(imagen.imagen.getScaledInstance(400, 400, Image.SCALE_SMOOTH));
            canvas.setIcon(icon);
        }
    }

    private void cargarImagen() {
        JFileChooser fileChooser = new JFileChooser();
        if (fileChooser.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
            try {
                imagen.cargar(fileChooser.getSelectedFile().getAbsolutePath());
                mostrarImagen();
            } catch (IOException ex) {
                JOptionPane.showMessageDialog(this, "Error al cargar la imagen.");
            }
        }
    }

    private void aplicarFiltro(Filtro filtro) {
        if (imagen.imagen != null) {
            filtro.aplicar(imagen);
            mostrarImagen();
        } else {
            JOptionPane.showMessageDialog(this, "Primero debes cargar una imagen.");
        }
    }

    private void guardarImagen() {
        if (imagen.imagen != null) {
            JFileChooser fileChooser = new JFileChooser();
            if (fileChooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
                try {
                    imagen.guardar(fileChooser.getSelectedFile().getAbsolutePath());
                    JOptionPane.showMessageDialog(this, "Imagen guardada correctamente.");
                } catch (IOException ex) {
                    JOptionPane.showMessageDialog(this, "Error al guardar la imagen.");
                }
            }
        } else {
            JOptionPane.showMessageDialog(this, "No hay imagen para guardar.");
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(EditorImagenApp::new);
    }
}
