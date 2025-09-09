        function x_y(y) {
                    let u_1 = Math.random();
                    let delta1 = Math.sqrt(Math.max((4 * (y ** 2)) + (12 * y) + 4 + (32 * u_1) + (24 * y * u_1), 0));
                    return ((-(3 * y) - 2 + delta1) / 2);
                }

        function y_x(x) {
            let u= Math.random();
            let delta2 = Math.sqrt(Math.max((x ** 2) + (2 * x) + 1 + (6 * u * x) + (15 * u), 0));
            return ((-(2 * x) - 2 + (2 * delta2)) / 3);
        }

        function gebbs(n, x, y) {
            let x0 = x;
            let y0 = y;
            let samples = [[x0, y0]];

            for (let i = 0; i < n; i++) {
                let x_n = x_y(samples[i][1]);
                let y_n = y_x(samples[i][0]);
                samples.push([x_n, y_n]);
            }
            return samples;
        }
        document.addEventListener("DOMContentLoaded", function() {
            const form = document.getElementById("formulario");
            if (form) {
                form.addEventListener("submit", function(e) {
                    e.preventDefault();

                    const x = Number(document.getElementById('x').value);
                    const y = Number(document.getElementById('y').value);
                    const n = Number(document.getElementById('n').value);

                    // Validar inputs
                    if (isNaN(x) || isNaN(y) || isNaN(n)) {
                        alert("Por favor ingresa valores numéricos válidos");
                        return;
                    }

                    // Calcular muestras
                    let samples = gebbs(n, x, y);

                    // Preparar datos para la gráfica
                    let x_vals = samples.map(p => p[0]);
                    let y_vals = samples.map(p => p[1]);
                    let z_vals = samples.map((p, i) => 1);

                    // Crear traza 3D
                    let trace = {
                        x: x_vals,
                        y: y_vals,
                        z: z_vals,
                        mode: 'markers',
                        type: 'scatter3d',
                        marker: { 
                            size: 3, 
                            color: z_vals, 
                            colorscale: 'Viridis',
                            opacity: 0.8
                        }
                    };

                    let hist2d = {
                            x: x_vals,
                            y: y_vals,
                            type: "histogram2d",
                            colorscale: "Viridis"
                        };

                        Plotly.newPlot("grafica3d", [hist2d]);

                    // Configuración del layout
                    let layout = {
                        margin: { l: 0, r: 0, b: 0, t: 0 },
                        scene: {
                            xaxis: { title: 'X' },
                            yaxis: { title: 'Y' },
                            zaxis: { title: 'Iteración' },
                            camera: {
                                eye: { x: 1.5, y: 1.5, z: 1.5 }
                            }
                        }
                    };

                    // Dibujar gráfica
                    Plotly.newPlot('grafica3d', [trace], layout);
                    Plotly.newPlot("histo3d", [hist2d]);
                });
            }
        });