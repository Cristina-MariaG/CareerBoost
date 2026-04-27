import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import PostResult from '../components/PostResult.vue'

describe('PostResult', () => {
  it('renders nothing when content is empty and not streaming', () => {
    const wrapper = mount(PostResult, {
      props: { content: '', streaming: false },
    })
    expect(wrapper.find('.output-card').exists()).toBe(false)
  })

  it('shows spinner when streaming with no content yet', () => {
    const wrapper = mount(PostResult, {
      props: { content: '', streaming: true },
    })
    expect(wrapper.find('.spinner').exists()).toBe(true)
  })

  it('renders markdown content when provided', () => {
    const wrapper = mount(PostResult, {
      props: { content: '**Hello world**', streaming: false },
    })
    expect(wrapper.find('.output-body').html()).toContain('<strong>')
  })

  it('shows copy button when content is present', () => {
    const wrapper = mount(PostResult, {
      props: { content: 'some post content here', streaming: false },
    })
    expect(wrapper.find('.copy-btn').exists()).toBe(true)
  })
})
