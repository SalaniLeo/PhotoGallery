<script lang="ts">
	let email = '',
		password = '',
		error = '';

	export let form;
	export let data;
</script>

<form method="POST">
	<div class="root">
		<div class="container">
			<div class="left">
				<h3>Log In - or <a href="/auth/register">Sign In</a></h3>
				<div class="content">
					<div class="inputs">
						<input
							type="text"
							id="email"
							name="email"
							placeholder="Email"
							style="border-bottom: 2px solid {form?.state};"
							bind:value={email}
						/>
						<input
							type="password"
							id="password"
							name="password"
							placeholder="Password"
							style="border-bottom: 2px solid {form?.state};"
							bind:value={password}
						/>
					</div>
					<div class="errorslot">
						{#if form?.error}
							<small style="color: {form?.state};">{form?.error}</small>
						{/if}
					</div>
					<div class="oauth"></div>
				</div>
				<div class="ralign">
					<button type="submit">Log In</button>
				</div>
			</div>
			<div class="right">
				{#await data['latest_post']}
					<p>Loading..</p>
				{:then latest}
					{#if latest}
						<div class="image">
							<img src={`${data['address']}/static/${latest['source']}.jpg`} alt="Latest post" />
						</div>
					{/if}
				{/await}
			</div>
		</div>
	</div>
</form>

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
	.root {
		padding: 25px;
		display: flex;
		justify-content: center;
		align-items: center;
	}
	.container {
		padding: 0px;
		width: max-content;
		height: fit-content;
		border-radius: var(--border-radius-heavy);
		background-color: var(--secondary-color);
		display: flex;
		flex-direction: row;
		overflow: hidden;
	}
	.container > .left {
		padding: 1rem;
		width: 40%;
		min-width: 250px;
		display: flex;
		flex-direction: column;
		gap: 10px;
	}
	.container > .right {
		background-color: var(--tertiary-color);
		width: 60%;
		padding: 1.5rem;
	}
	.left > .content {
		height: 100%;
		display: flex;
		flex-direction: column;
		gap: 20px;
		align-items: unset;
		justify-self: unset;
	}
	.left > .content > .errorslot {
		height: 0px;
		transform: translateY(-12.5px);
	}
	.left > .content > .inputs {
		display: flex;
		flex-direction: column;
		gap: 20px;
	}
	.left > .content > .oauth {
		display: flex;
		flex-direction: column;
		gap: 20px;
	}
	.left h3 {
		margin: 15px;
	}
	.ralign {
		display: flex;
		justify-content: right;
		align-items: center;
	}
	@media screen and (max-width: 1200px) {
		.root {
			display: flex;
			flex-direction: row;
			overflow: hidden;
			width: unset;
			margin-left: 2rem;
			margin-right: 2rem;
		}
	}
	@media screen and (max-width: 1000px) {
		/* .right{
		display: none;
	} */
	}
	@media screen and (max-width: 720px) {
		.root {
			margin-left: 0.5rem;
			margin-right: 0.5rem;
		}
		.right {
			display: none;
		}
		.left {
			width: 100% !important;
		}
	}
</style>
