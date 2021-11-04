<template>
  <div
      class="d-flex flex-column ml-5 mr-5"
      :style="deploy_form_visible? '': 'display: none !important;'"
  >
    <v-form
        ref="deploy_form"
        v-model="deploy_form_valid"
        lazy-validation
    >
      <v-text-field
          class=""
          style=""
          v-model="jobname"
          :rules="[v => !!v || 'A name is required', v => (v && v.length >= 5) || 'Name must at least 5 characters']"
          label="Enter the job name"
          hide-details="auto"
          :color="color"
          :disabled="jobname_disabled"
          dense
          outlined
          filled
          counter
          :maxlength="25"
          @change="jobname_change"
      >
      </v-text-field>
      <v-text-field
          class="mt-5 mb-5"
          style=""
          v-model="frequency"
          :rules="[v => !!v || 'A frequency is required',
        v => (v && !!/^every \d+ \w+$/.test(frequency.toLowerCase())) ||
        'Provide a valid Cron expression, i.e. `every 15 minutes`']"
          label="Enter the job frequency"
          hide-details="auto"
          :color="color"
          :disabled="frequency_disabled"
          dense
          outlined
          filled
          counter
          :maxlength="25"
          @change="frequency_change"
      >
      </v-text-field>
    </v-form>

  </div>
</template>
<script>
module.exports = {
  mounted() {
    this.$refs.deploy_form.validate()
  }
}
</script>