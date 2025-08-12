<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card
      class="q-dialog-plugin q-pa-lg shadow-24 relative-position"
      style="
        background: #1f2937;
        width: 50vw;
        max-width: 80vw;
        height: 40vh;
        max-height: 100vh;
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

      <q-card-section class="absolute-bottom q-pb-xl">
        <q-form class="row justify-around">
          <div class="row">
            <q-input
              filled
              v-model="dateModel"
              label="Selecione a Data"
              class="cursor-pointer"
              style="background: white; border-radius: 30px"
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
              v-model="dateModel"
              label="Selecione a Data"
              class="cursor-pointer"
              style="background: white; border-radius: 30px"
            >
              <template v-slot:append>
                <q-icon name="event">
                  <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                    <q-date v-model="dateModel" minimal />
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
          </div>

          <div class="q-pl-md">
            <q-btn color="green-7" label="Solicitar Reserva" type="submit" size="lg" rounded />
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { useDialogPluginComponent } from 'quasar';
import { ref } from 'vue';

const dateModel = ref('');

const props = defineProps({
  roomName: {
    type: String,
    required: true,
  },
});

defineEmits([...useDialogPluginComponent.emits]);

const { dialogRef, onDialogHide, onDialogCancel } = useDialogPluginComponent();

function goBack() {
  onDialogCancel();
}
</script>
