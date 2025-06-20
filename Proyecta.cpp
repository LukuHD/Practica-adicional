#include <iostream>
#include <opencv2/opencv.hpp>

// Clase base abstracta Filtro
class Filtro {
public:
    virtual void aplicar(cv::Mat& imagen) = 0; // Método puro virtual
    virtual ~Filtro() {}
};

// Filtro Grises
class FiltroGrises : public Filtro {
public:
    void aplicar(cv::Mat& imagen) override {
        cv::cvtColor(imagen, imagen, cv::COLOR_BGR2GRAY);
        cv::cvtColor(imagen, imagen, cv::COLOR_GRAY2BGR); // Para mantener 3 canales
    }
};

// Filtro Inversión
class FiltroInversion : public Filtro {
public:
    void aplicar(cv::Mat& imagen) override {
        cv::bitwise_not(imagen, imagen);
    }
};

// Clase Imagen
class Imagen {
private:
    cv::Mat img;
    std::string ruta;

public:
    bool cargar(const std::string& rutaArchivo) {
        ruta = rutaArchivo;
        img = cv::imread(rutaArchivo);
        return !img.empty();
    }

    bool guardar(const std::string& rutaGuardar) {
        if (img.empty()) return false;
        return cv::imwrite(rutaGuardar, img);
    }

    void mostrar(const std::string& ventana) {
        if (!img.empty()) {
            cv::imshow(ventana, img);
            cv::waitKey(0);
            cv::destroyWindow(ventana);
        }
    }

    cv::Mat& obtenerMat() {
        return img;
    }
};

// Menú básico en consola
int main() {
    Imagen imagen;
    std::string ruta;

    std::cout << "Ingrese la ruta de la imagen: ";
    std::getline(std::cin, ruta);

    if (!imagen.cargar(ruta)) {
        std::cerr << "No se pudo cargar la imagen.\n";
        return 1;
    }

    int opcion;
    std::cout << "Seleccione un filtro:\n";
    std::cout << "1. Escala de Grises\n";
    std::cout << "2. Inversión de Colores\n";
    std::cout << "Opción: ";
    std::cin >> opcion;

    Filtro* filtro = nullptr;
    switch (opcion) {
        case 1:
            filtro = new FiltroGrises();
            break;
        case 2:
            filtro = new FiltroInversion();
            break;
        default:
            std::cerr << "Opción inválida.\n";
            return 1;
    }

    filtro->aplicar(imagen.obtenerMat());
    imagen.mostrar("Imagen con filtro aplicado");

    std::string rutaSalida;
    std::cout << "Ingrese la ruta para guardar la imagen: ";
    std::cin.ignore();
    std::getline(std::cin, rutaSalida);

    if (imagen.guardar(rutaSalida)) {
        std::cout << "Imagen guardada con éxito en " << rutaSalida << "\n";
    } else {
        std::cerr << "Error al guardar la imagen.\n";
    }

    delete filtro;
    return 0;
}