<template>
  <v-card
      class="ml-5 mr-5 mb-5"
      :style="model_action_visible?'background-color:#F6F6F6; opacity: 1; min-width: 300px': 'display: none !important'"
  >
    <v-card-title>
      Model Action
    </v-card-title>
    <v-select
        class="ml-5 mr-5"
        style=""
        label="Select action to apply to the model"
        dense
        outlined
        filled
        :disabled="action_disabled"
        :color="color"
        :item-color="color"
        :items="['Investigate', 'Deploy']"
        v-model="selection"
        @change="action_change"
    >
    </v-select>
    <v-form
        ref="investigation_form"
        v-model="investigation_form_valid"
        lazy-validation
    >
      <v-text-field
          class="ml-5 mr-5 mb-5"
          style=""
          v-model="result_name"
          :rules="[v => !!v || 'A name is required', v => (v && v.length >= 5) || 'Name must at least 5 characters']"
          label="Enter the name of the result signal"
          hide-details="auto"
          :color="color"
          :disabled="result_name_disabled"
          dense
          outlined
          filled
          counter
          :maxlength="25"
          @change="result_name_change"
      >
      </v-text-field>

    </v-form>

    <investigate_widget></investigate_widget>
    <deploy_widget></deploy_widget>
  </v-card>
</template>

<script>
module.exports = {
  mounted() {
    this.$refs.investigation_form.validate()
  }
}
</script>