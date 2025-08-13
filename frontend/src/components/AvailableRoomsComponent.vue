<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card
      class="q-dialog-plugin q-pa-lg shadow-24"
      style="
        background: #1f2937;
        width: 42vw;
        max-width: 80vw;
        height: 55vh;
        max-height: 100vh;
        border: 1px solid #30363d;
        border-radius: 20px;
      "
    >
      <q-card-actions align="left">
        <q-btn flat round icon="arrow_back" color="blue-grey-2" @click="goBack" />
        <div class="text-h6 text-white q-ml-sm">{{ props.roomType }} Disponíveis</div>
      </q-card-actions>

      <q-card-section>
        <q-list class="q-gutter-md">
          <q-item
            clickable
            v-ripple
            class="bg-dark-2 q-py-lg"
            style="background: #2b3544; border: 1px solid #30363d; border-radius: 10px"
          >
            <q-item-section>
              <q-item-label class="text-white text-bold" style="font-size: 18px"
                >Auditório CT I</q-item-label
              >
              <q-item-label caption class="text-blue-grey-4">Capacidade: 100 pessoas</q-item-label>
            </q-item-section>

            <q-item-section side>
              <q-btn
                unelevated
                size="lg"
                color="green-7"
                label="Reservar"
                @click="reserve('Auditório CT I')"
              />
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { useDialogPluginComponent, Dialog } from 'quasar';
import AppointmentComponent from './AppointmentComponent.vue';

const props = defineProps({
  roomType: {
    type: String,
    required: true,
  },
});

defineEmits([...useDialogPluginComponent.emits]);

const { dialogRef, onDialogHide, onDialogCancel } = useDialogPluginComponent();

function goBack() {
  onDialogCancel();
}

function reserve(room) {
  Dialog.create({
    component: AppointmentComponent,

    componentProps: {
      roomName: room,
    },
  })
    .onOk(() => {
      console.log('OK');
    })
    .onCancel(() => {
      console.log('Cancel');
    })
    .onDismiss(() => {
      console.log('OK or Cancel');
    });
}
</script>
