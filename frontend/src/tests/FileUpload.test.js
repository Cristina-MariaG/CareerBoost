import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import FileUpload from '../components/FileUpload.vue'

describe('FileUpload', () => {
  it('renders label and icon', () => {
    const wrapper = mount(FileUpload, {
      props: { label: 'Ton CV (PDF)', icon: '📄' },
    })
    expect(wrapper.text()).toContain('Ton CV (PDF)')
  })

  it('rejects non-PDF files', async () => {
    const wrapper = mount(FileUpload, {
      props: { label: 'Ton CV', icon: '📄' },
    })
    const file = new File(['content'], 'doc.txt', { type: 'text/plain' })
    const input = wrapper.find('input[type="file"]')
    Object.defineProperty(input.element, 'files', { value: [file] })
    await input.trigger('change')
    expect(wrapper.text()).toContain('PDF')
  })

  it('applies disabled styling when disabled prop is true', () => {
    const wrapper = mount(FileUpload, {
      props: { label: 'Ton CV', icon: '📄', disabled: true },
    })
    expect(wrapper.find('.drop-zone').classes()).toContain('drop-zone--disabled')
  })
})
