        let currentView = 'dual'; // 'dual' o 'histogram2d'
        let currentSamples = [];
        let currentDistribution = window.flaskData.currentDistribution;

        // csv
        function downloadCsv(data, filename) {
            const blob = new Blob([data], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            setTimeout(() => {
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }, 100);
        }

        // Funcion para calcular histograma 2D
        function calculate2DHistogram(x, y, bins) {
            const xMin = Math.min(...x);
            const xMax = Math.max(...x);
            const yMin = Math.min(...y);
            const yMax = Math.max(...y);
            
            const xBinSize = (xMax - xMin) / bins;
            const yBinSize = (yMax - yMin) / bins;
            
            const counts = Array(bins).fill().map(() => Array(bins).fill(0));
            
            for (let i = 0; i < x.length; i++) {
                const xBin = Math.min(bins - 1, Math.floor((x[i] - xMin) / xBinSize));
                const yBin = Math.min(bins - 1, Math.floor((y[i] - yMin) / yBinSize));
                counts[xBin][yBin]++;
            }
            
            const xCenters = [];
            const yCenters = [];
            
            for (let i = 0; i < bins; i++) {
                xCenters.push(xMin + (i + 0.5) * xBinSize);
                yCenters.push(yMin + (i + 0.5) * yBinSize);
            }
            
            return {
                x: xCenters,
                y: yCenters,
                z: counts
            };
        }
        // aqui en adelante esta lo de gibbs el we que cache que le movio  a la simulacion de gibbs y modifico los puntos y las simulaciones lo hago 
        // a que haga las simulaciones desde cero, no metan toda la bendita funcion al claude que luego hace estupideces y no sirve gracias por su atencion
        //no lo hagan porfa

        // Funciones para Gebbs - Función de ejemplo f(x,y) = 2
        function x_given_y_ejemplo(y) {
            // f(x|y) = u(1-y) donde u es uniforme en [0, x/(1-y)]
            let u = Math.random();
            return u * (1 - y);
        }

        function y_given_x_ejemplo(x) {
            // f(y|x) = u(1-x) donde u es uniforme en [0, x/(1-y)]
            let u = Math.random();
            return u * (1 - x);
        }

        function gebbs_ejemplo(n, x, y) {
            let x0 = x;
            let y0 = y;
            let samples = [[x0, y0]];

            for (let i = 0; i < n; i++) {
                let x_n = x_given_y_ejemplo(samples[i][1]);
                let y_n = y_given_x_ejemplo(x_n);
                samples.push([x_n, y_n]);
            }
            return samples;
        }

        // Funciones para Gebbs - Función original
        function x_y(y) {
                let u = Math.random();
                const discriminant = 4 * (y*y + 3*y + 1 + u*(6*y + 8));
                return (-3*y - 2 + Math.sqrt(Math.max(0, discriminant))) / 2;
            }

        function y_x(x) {
                let u = Math.random();
                const base = x + 1;
                const discriminant = base*base + 3*u*(2*x + 5);
                return 2*(-base + Math.sqrt(Math.max(0, discriminant))) / 3;
            }

        function gebbs(n, x, y) {
            let x0 = x;
            let y0 = y;
            let samples = [[x0, y0]];

            for (let i = 0; i < n; i++) {
                let x_n = x_y(samples[i][1]);
                let y_n = y_x(x_n);
                samples.push([x_n, y_n]);
            }
            return samples;
        }

        // Funciones para Normal Bivariada
        function normal(n, mu, sigma) {
            let x = [];
            for (let i = 0; i < n; i++) {
                let u1 = Math.random();
                let u2 = Math.random();
                let z0 = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
                x.push(z0 * sigma + mu);
            }
            return x;
        }

        // Nueva función para alternar vistas
        function toggleView() {
            const dualView = document.getElementById('dual-view');
            const singleView = document.getElementById('single-view');
            const buttonIcon = document.getElementById('button-icon');
            const buttonText = document.getElementById('button-text');

            if (currentView === 'dual') {
                // Cambiar a vista de histograma 2D
                currentView = 'histogram2d';
                dualView.classList.add('chart-hidden');
                singleView.classList.remove('chart-hidden');
                buttonIcon.textContent = '🎯';
                buttonText.textContent = 'Ver Gráficos 3D';
                
                // Crear histograma 2D si hay datos
                if (currentSamples.length > 0) {
                    createHistogram2D();
                }
            } else {
                // Cambiar a vista dual
                currentView = 'dual';
                singleView.classList.add('chart-hidden');
                dualView.classList.remove('chart-hidden');
                buttonIcon.textContent = '📊';
                buttonText.textContent = 'Ver Histograma 2D';
            }
        }

        // Función para crear histograma 2D
        function createHistogram2D() {
            if (currentDistribution === '2normal') {
                const x_vals = currentSamples.map(p => p[0]);
                const y_vals = currentSamples.map(p => p[1]);
                
                let hist2d = {
                    x: x_vals,
                    y: y_vals,
                    type: "histogram2d",
                    colorscale: "Viridis",
                    name: 'Histograma 2D'
                };
                
                const layout = {
                    margin: { l: 40, r: 20, b: 40, t: 20 },
                    xaxis: { title: 'X' },
                    yaxis: { title: 'Y' }
                };
                
                Plotly.newPlot("histo2d", [hist2d], layout);
            } else if (currentDistribution === 'gebbs') {
                // Para Gibbs, crear histograma 2D de las posiciones
                const x_vals = currentSamples.map(p => p[0]);
                const y_vals = currentSamples.map(p => p[1]);
                
                let hist2d = {
                    x: x_vals,
                    y: y_vals,
                    type: "histogram2d",
                    colorscale: "Viridis",
                    name: 'Histograma 2D'
                };
                
                const layout = {
                    margin: { l: 40, r: 20, b: 40, t: 20 },
                    xaxis: { title: 'X' },
                    yaxis: { title: 'Y' }
                };
                
                Plotly.newPlot("histo2d", [hist2d], layout);
            }
        }

        // Función para crear los gráficos duales
        function createDualCharts() {
            if (currentDistribution === 'gebbs') {
                // Gráfico 3D scatter
                let trace3d = {
                    x: currentSamples.map(p => p[0]),
                    y: currentSamples.map(p => p[1]),
                    z: currentSamples.map(p => 1),
                    mode: 'markers',
                    type: 'scatter3d',
                    marker: { 
                        size: 3, 
                        color: currentSamples.map((p, i) => i), 
                        colorscale: 'Viridis',
                        opacity: 0.8
                    },
                    name: 'Muestras Gibbs'
                };

                const layout3d = {
                    margin: { l: 10, r: 10, b: 10, t: 10 },
                    scene: {
                        xaxis: { title: 'X' },
                        yaxis: { title: 'Y' },
                        zaxis: { title: 'Iteración' },
                        camera: { eye: { x: 1.5, y: 1.5, z: 1.5 } }
                    }
                };

                Plotly.newPlot('grafica3d', [trace3d], layout3d);

                // Histograma 3D
                const histogramData = calculate2DHistogram(
                    currentSamples.map(p => p[0]), 
                    currentSamples.map(p => p[1]), 
                    20
                );
                
                let histogram3DTrace = {
                    x: histogramData.x,
                    y: histogramData.y,
                    z: histogramData.z,
                    type: 'surface',
                    colorscale: 'Viridis',
                    opacity: 0.8,
                    name: 'Histograma 3D'
                };
                
                Plotly.newPlot('histograma3d', [histogram3DTrace], layout3d);

            } else if (currentDistribution === '2normal') {
                const x_vals = currentSamples.map(p => p[0]);
                const y_vals = currentSamples.map(p => p[1]);

                // Gráfico 3D scatter
                let trace3d = {
                    x: x_vals,
                    y: y_vals,
                    z: Array(x_vals.length).fill(0.5),
                    mode: 'markers',
                    type: 'scatter3d',
                    marker: {
                        size: 3,
                        color: Array(x_vals.length).fill(0.5),
                        colorscale: 'Viridis',
                        opacity: 0.8
                    },
                    name: 'Muestras Normales'
                };

                const layout3d = {
                    margin: { l: 10, r: 10, b: 10, t: 10 },
                    scene: {
                        xaxis: { title: 'X' },
                        yaxis: { title: 'Y' },
                        zaxis: { title: 'Z' },
                        camera: { eye: { x: 1.5, y: 1.5, z: 1.5 } }
                    }
                };

                Plotly.newPlot('grafica3d', [trace3d], layout3d);

                // Histograma 3D
                const histogramData = calculate2DHistogram(x_vals, y_vals, 20);
                
                let histogram3DTrace = {
                    x: histogramData.x,
                    y: histogramData.y,
                    z: histogramData.z,
                    type: 'surface',
                    colorscale: 'Viridis',
                    opacity: 0.8,
                    name: 'Histograma 3D'
                };
                
                Plotly.newPlot('histograma3d', [histogram3DTrace], layout3d);
            }
        }

        //PUROS CORRIDOS TUMBADOS VIEJILLO🗣️🗣️🗣️
        // descarga

        // el codigo que hizo goprge esta bien pero le falta una cosa
        // que es poner un boton para poner una funcion de ejemplo 
        // y que el usuario pueda ver como funciona la simulacion
        // solo es agregar un boton que haga eso
        // si de pura ciripa debemos agregar otro pus namas se cambia el estado y se agrega otro boton mas 
        
        let estadoEjemplo = false;
        document.addEventListener("DOMContentLoaded", function() {
            const form = document.getElementById("formulario");
            const downloadCard = document.getElementById("download-card");
            const downloadBtn = document.getElementById("download-btn");
            const ejemploBtn = document.getElementById("ejemplo-btn");

            if(ejemploBtn){// busca si existe este elemeto cuando se cambia de simulacion esto sirve para saber si extiste o no
                ejemploBtn.addEventListener("click", function() {
                    estadoEjemplo = !estadoEjemplo; // cada que se haga click cambia el estado de la variable
                    if (estadoEjemplo) {
                        ejemploBtn.textContent = "📝 Usando función de ejemplo: f(x,y) = 2 para x+y≤1, x≥0, y≥0 (Haz clic para desactivar)";
                        ejemploBtn.dataset.ejemplo = 'true';
                    } else {
                        ejemploBtn.textContent = "📝 Probar función de ejemplo: f(x,y) = 2 para x+y≤1, x≥0, y≥0";
                        ejemploBtn.dataset.ejemplo = 'false';
                    }
                });

            }


            if (form) {
                form.addEventListener("submit", function(e) {
                    e.preventDefault();
                    
                    if (currentDistribution === 'gebbs') {
                        const x = Number(document.getElementById('x').value);
                        const y = Number(document.getElementById('y').value);
                        const n = Number(document.getElementById('n').value);

                        if (isNaN(x) || isNaN(y) || isNaN(n)) {
                            alert("Por favor ingresa valores numericos validos");
                            return;
                        }
                        // pasamos la data dependiendo de que estado este la variable asi evitamos hacer otro formulario
                        // como se mantiene las variables podemos hacer eso 
                        
                        if (estadoEjemplo) {
                                currentSamples = gebbs_ejemplo(n, x, y);
                                createDualCharts();
                        } else {
                                currentSamples = gebbs(n, x, y);
                                createDualCharts();
                        }
                            
                            
                            
                        
                        
                    } else if (currentDistribution === '2normal') {
                        const rho = parseFloat(document.getElementById('rho').value);
                        const mu1 = parseFloat(document.getElementById('miu1').value);
                        const mu2 = parseFloat(document.getElementById('miu2').value);
                        const sigma1 = parseFloat(document.getElementById('sigma1').value);
                        const sigma2 = parseFloat(document.getElementById('sigma2').value);
                        const n = parseInt(document.getElementById('n').value);

                        if (isNaN(rho) || isNaN(mu1) || isNaN(mu2) || isNaN(sigma1) || isNaN(sigma2) || isNaN(n)) {
                            alert("Por favor ingresa valores numericos validos");
                            return;
                        }

                        let z1 = normal(n, 0, 1);
                        let z2 = normal(n, 0, 1);

                        let x_vals = [];
                        let y_vals = [];
                        
                        for (let i = 0; i < n; i++) {
                            let x = mu1 + sigma1 * z1[i];
                            let y = mu2 + rho * (sigma2/sigma1) * (x - mu1) + sigma2 * Math.sqrt(1 - rho*rho) * z2[i];
                            x_vals.push(x);
                            y_vals.push(y);
                        }

                        currentSamples = x_vals.map((x, i) => [x, y_vals[i]]);
                        createDualCharts();
                    }
                    
                    downloadCard.style.display = 'block';
                });
            }

            if (downloadBtn) {
                downloadBtn.addEventListener("click", function() {
                    if (currentSamples.length === 0) {
                        alert("No hay datos para descargar. Primero ejecuta la simulacion.");
                        return;
                    }
                    
                    let csvData = "";
                    if (currentDistribution === 'gebbs') {
                        // Encabezados CSV
                        csvData = "Iteracion,Valor_X,Valor_Y\n";
                        // Datos
                        currentSamples.forEach((sample, index) => {
                            csvData += `${index},${sample[0].toFixed(6)},${sample[1].toFixed(6)}\n`;
                        });
                    } else if (currentDistribution === '2normal') {
                        // Encabezados CSV
                        csvData = "Muestra,Valor_X,Valor_Y\n";
                        // Datos
                        currentSamples.forEach((sample, index) => {
                            csvData += `${index},${sample[0].toFixed(6)},${sample[1].toFixed(6)}\n`;
                        });
                    }
                    
                    downloadCsv(csvData, `simulacion_${currentDistribution}.csv`);
                });
            }
        });