import { Component, OnInit, OnDestroy, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgChartsModule } from 'ng2-charts';
import { ChartData, ChartOptions } from 'chart.js';
import { SensorService } from '../../services/sensor.service';

@Component({
  selector: 'app-grafico',
  standalone: true,
  imports: [CommonModule, NgChartsModule],
  templateUrl: './grafico.html'
})
export class GraficoComponent implements OnInit, OnDestroy {

  intervalo: any;
  labels: string[] = [];  // Tiempos para el eje X
  dataPorSensor: { [id: number]: number[] } = {};  // Historial por ID del sensor

  chartLabels = signal<string[]>([]);
  chartData = signal<ChartData<'line'>>({
    labels: [],
    datasets: []
  });

  chartOptions: ChartOptions = {
    responsive: true,
    plugins: {
      legend: { display: true },
      tooltip: { enabled: true },
      title: {
        display: true,
        text: 'Valores de Sensores Simulados',
        font: { size: 18 }
      }
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Tiempo'
        }
      },
      y: {
         min: 0,
      max: 100,
        title: {
          display: true,
          text: 'Valor'
        }
      }
    }
  };

  constructor(private sensorService: SensorService) {}

  todosLosSensores = [
    { id: 1, nombre: 'Sensor A' },
    { id: 2, nombre: 'Sensor B' },
    { id: 3, nombre: 'Sensor C' },
  ];

  sensoresSeleccionados = signal<number[]>([1, 2, 3]);

  ngOnInit(): void {
    this.intervalo = setInterval(() => this.actualizarDatos(), 2000);
  }

  actualizarDatos(): void {
    const hora = new Date().toLocaleTimeString();
    this.labels.push(hora);
    if (this.labels.length > 30) this.labels.shift();

    const ids = this.sensoresSeleccionados();

    this.sensorService.obtenerValores(ids).subscribe(datos => {
      datos.forEach((sensor, index) => {
        const id = ids[index]; // Relación por posición de solicitud

        if (!this.dataPorSensor[id]) {
          this.dataPorSensor[id] = [];
        }

        const arr = this.dataPorSensor[id];
        arr.push(sensor.value);
        if (arr.length >330) arr.shift();
      });

      this.chartLabels.set([...this.labels]);
      this.chartData.set({
        labels: [...this.labels],
        datasets: this.sensoresSeleccionados().map(id => ({
          data: this.dataPorSensor[id] || [],
          label: this.obtenerNombreSensor(id)
        }))
      });
    });
  }

  onSeleccionCambio(event: Event): void {
    const selected = Array.from((event.target as HTMLSelectElement).selectedOptions)
      .map(option => Number(option.value));
    this.sensoresSeleccionados.set(selected);

    
  }

  obtenerNombreSensor(id: number): string {
    const sensor = this.todosLosSensores.find(s => s.id === id);
    return sensor ? sensor.nombre : `Sensor ${id}`;
  }

  chartDataPorSensor(id: number): ChartData<'line'> {
    const valores = this.dataPorSensor[id];
    return {
      labels: [...this.labels],
      datasets: [{
        data: valores,
        label: this.obtenerNombreSensor(id)
      }]
    };
  }

  ngOnDestroy(): void {
    clearInterval(this.intervalo);
  }
}
