<script lang="ts">
	async function get_latest() {
		const response = await fetch('http://127.0.0.1:5000/api/get_latest_post', {
			method: 'GET'
		});

		let data = await response.json();
		return data;
	}
</script>

<div class="root">
	{#await get_latest()}
		<p>Loading..</p>
	{:then latest}
		<div class="image">
			<img src={`http://127.0.0.1:5000/static/${latest['source']}.jpg`} alt="Latest post" />
		</div>
	{/await}
</div>

<style>
	.image {
		display: flex;
		justify-content: center;
	}
	img {
		display: block;
		max-width: 40vw; /* Maximum width */
		max-height: 320px; /* Maximum height */
		width: auto; /* Maintain aspect ratio */
		height: auto; /* Maintain aspect ratio */
		object-fit: scale-down; /* or object-fit: cover; */
		border-radius: var(--border-radius-medium);
	}
</style>
