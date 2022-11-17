<template>
  <div class="container">
    <Bar v-if="loaded" :chart-data="chartData" :chart-options="chartOptions" />
    <p v-if="!loaded">Cargando Estadísticas</p>
  </div>
</template>

<script lang="ts">
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  SubTitle,
} from 'chart.js'
import { Discipline } from '../interfaces/Discipline'
import { getAssociates } from '../services/AssociateDataService'
import { defineComponent } from 'vue'

ChartJS.register(
  Title,
  SubTitle,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
)

export default defineComponent({
  name: 'BarChart',
  components: { Bar },
  data() {
    return {
      loaded: false,
      chartData: { datasets: [] as any, labels: [] as any },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Cantidad de inscriptos a disciplinas por género',
            font: { size: 24 },
          },
          subtitle: {
            display: true,
            text: '',
            font: { size: 14 },
          },
        },
        scales: {
          x: {
            stacked: true,
            barThickness: 0.1,
          },
          y: {
            stacked: true,
            ticks: {
              beginAtZero: true,
              callback: function (value: number) {
                if (value % 1 === 0) {
                  return value
                }
              },
            },
          },
        },
      },
    }
  },
  async mounted() {
    this.loaded = false
    try {
      const res = await getAssociates()

      const labelList = Array.from(
        {
          length:
            Number(res.years[1]) - Number(res.years[0]) < 10
              ? 10
              : Number(res.years[1]) - Number(res.years[0]) + 1,
        },
        (_, i) => String(Number(res.years[0]) + i)
      )
      let countdict = {} as { [key: number]: number }
      labelList.forEach((year) => (countdict[Number(year)] = 0))
      res.data.map((assoc) =>
        assoc.disciplines!.map((discip: Discipline) => {
          let d = new Date(discip.associated_at!).getFullYear()
          countdict[d] += 1
        })
      )

      let dict = {} as { [key: string]: { [key: string]: number } }
      res.data.map((assoc) =>
        assoc.disciplines!.map((discip: Discipline) => {
          let d = new Date(discip.associated_at!).getFullYear()
          if (dict[assoc.gender] == undefined) {
            dict[assoc.gender] = {}
            labelList.forEach((year) => (dict[assoc.gender][Number(year)] = 0))
          }
          dict[assoc.gender][d] += 1
        })
      )

      const currentYear = new Date(Date.now()).getFullYear()
      const associatesSinceLastYear = countdict[currentYear - 1]
        ? countdict[currentYear] - countdict[currentYear - 1]
        : countdict[currentYear]

      if (countdict[currentYear - 1] == undefined) {
        this.chartOptions.plugins.subtitle.text = `Se inscribieron ${associatesSinceLastYear} personas a disciplinas este año`
      } else {
        countdict[currentYear - 1] =
          countdict[currentYear - 1] == 0 ? 1 : countdict[currentYear - 1]
        this.chartOptions.plugins.subtitle.text =
          associatesSinceLastYear >= 0
            ? `Se inscribieron ${associatesSinceLastYear} más personas a disciplinas este año, un ${
                (associatesSinceLastYear / countdict[currentYear - 1]) * 100
              }% más inscriptos que el año pasado`
            : `Se inscribieron ${Math.round(
                Math.abs(associatesSinceLastYear)
              )} personas menos a disciplinas este año, un ${Math.round(
                Math.abs(
                  (associatesSinceLastYear / countdict[currentYear - 1]) * 100
                )
              )}% menos inscriptos que el año pasado`
      }

      this.chartData = {
        labels: labelList,
        datasets: [
          {
            label: 'Hombres',
            backgroundColor: '#ffad08',
            data: dict.male ? Object.values(dict.male) : [],
          },
          {
            label: 'Mujeres',
            backgroundColor: '#73b06f',
            data: dict.female ? Object.values(dict.female) : [],
          },
          {
            label: 'Otro',
            backgroundColor: '#405059',
            data: dict.other ? Object.values(dict.other) : [],
          },
        ],
      }

      this.loaded = true
    } catch (e) {
      console.error(e)
    }
  },
})
</script>