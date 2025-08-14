<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card
      class="q-dialog-plugin q-pa-lg shadow-24 relative-position"
      style="
        background: #1f2937;
        width: 60vw;
        max-width: 80vw;
        height: 60vh;
        max-height: 150vh;
        border: 1px solid #30363d;
        border-radius: 20px;
      "
    >
      <q-card-actions align="left">
        <q-btn flat round icon="arrow_back" color="blue-grey-2" @click="goBack" />
        <div class="text-h5 text-white q-ml-sm">{{ props.roomName }}</div>
      </q-card-actions>

      <q-card-section>
        <div class="text-h6 text-blue-grey-4">Capacidade: 100 pessoas</div>
        <div class="text-h6 text-blue-grey-4">Recursos: Ar condicionado, Projetor</div>
      </q-card-section>

      <q-card-section class="q-pt-md">
        <q-form class="column q-gutter-md">
          <div class="row justify-between">
            <q-input
              filled
              v-model="dateModel"
              label="Selecione a Data"
              class="cursor-pointer"
              style="background: white; border-radius: 30px; width: 30%"
            >
              <template v-slot:append>
                <q-icon name="event">
                  <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                    <q-date v-model="dateModel" minimal />
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
            <q-input
              filled
              v-model="timeModel"
              label="Horário de Início"
              class="cursor-pointer"
              style="background: white; border-radius: 30px; width: 30%"
            >
              <template v-slot:append>
                <q-icon name="access_time">
                  <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                    <q-time v-model="timeModel" format24h />
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
            <q-input
              filled
              v-model="endTimeModel"
              label="Horário de Fim"
              class="cursor-pointer"
              style="background: white; border-radius: 30px; width: 30%"
            >
              <template v-slot:append>
                <q-icon name="access_time">
                  <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                    <q-time v-model="endTimeModel" format24h />
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
          </div>

          <div class="row justify-center q-mt-md">
            <q-btn color="green-7" label="Solicitar Reserva" type="submit" size="lg" rounded />
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { useDialogPluginComponent } from 'quasar'
import { ref } from 'vue'

const dateModel = ref('')
const timeModel = ref('')
const endTimeModel = ref('')

const props = defineProps({
  roomName: {
    type: String,
    required: true,
  },
})

defineEmits([...useDialogPluginComponent.emits])

const { dialogRef, onDialogHide, onDialogCancel } = useDialogPluginComponent()

function goBack() {
  onDialogCancel()
}
</script>
