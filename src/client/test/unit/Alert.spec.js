import { mount } from '@vue/test-utils';
import { describe, expect, it } from 'vitest';
import Alert from '@/components/Alert.vue';

describe('Alert', () => {
  it('renders the message and Bootstrap status class', () => {
    const wrapper = mount(Alert, {
      props: {
        message: 'Ready',
        status: 'success',
      },
    });

    expect(wrapper.get('[role="alert"]').text()).toBe('Ready');
    expect(wrapper.get('[role="alert"]').classes()).toContain('alert-success');
  });
});
