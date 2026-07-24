<!-- app.vue -->
<template>
  <div style="font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
    <h2 style="color: #2d3748;">Nuxt 3 Storefront Target</h2>
    <p style="color: #718096;">Simulated web layout for automated RL pipeline optimization sweeps.</p>
    
    <div style="margin: 20px 0; padding: 15px; background: #f7fafc; border-radius: 6px;">
      <h4>Item: Developer Workspace Monitor</h4>
      <p style="font-weight: bold; color: #4a5568;">Price: $499.00</p>
      <button @click="triggerCheckout" style="background: #319795; color: white; border: none; padding: 10px 16px; border-radius: 4px; cursor: pointer;">
        🛒 Process Order Checkout
      </button>
    </div>

    <div v-if="log" :style="{ padding: '10px', borderRadius: '4px', background: isError ? '#fed7d7' : '#c6f6d5', color: isError ? '#9b2c2c' : '#22543d' }">
      <strong>Status Log:</strong> {{ log }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const log = ref('')
const isError = ref(false)

async function triggerCheckout() {
  log.value = 'Submitting order packet...'
  try {
    const data = await $fetch('/api/checkout')
    log.value = data.message
    isError.value = false
  } catch (err) {
    log.value = err.statusMessage || 'HTTP 500: Server Thread Deadlock reached.'
    isError.value = true
  }
}
</script>