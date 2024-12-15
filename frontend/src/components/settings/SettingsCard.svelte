<script lang="ts">
  import * as Card from '@/components/ui/card';
  interface Props {
    children?: import('svelte').Snippet;
  }

  let { children }: Props = $props();
</script>

<Card.Root class="hover:bg-accent">
  <Card.Content class="p-3">
    {@render children?.()}
  </Card.Content>
</Card.Root>
