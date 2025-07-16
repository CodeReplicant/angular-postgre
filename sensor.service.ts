import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface SensorData {
  sensor_name: string;
  behavior: string;
  value: number;
}

@Injectable({ providedIn: 'root' })
export class SensorService {
  private API_URL = 'http://localhost:8000'; // <- Corrección importante

  constructor(private http: HttpClient) {}

  obtenerValores(ids: number[]): Observable<SensorData[]> {
    const params = ids.map(id => `sensors=${id}`).join('&');
    return this.http.get<SensorData[]>(`${this.API_URL}/simulate?${params}`); // ruta sugerida para consumir endpoint GET
  }
}
