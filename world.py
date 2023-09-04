from spgecs.systems.system import SPGSystem
from typing import Type, TypeVar, Optional, Iterable, Set

T = TypeVar('T')

class World:
    def __init__(self) -> None:
        self.entities: dict[int, dict[Type[T], T]] = {}
        self.components: dict[Type(T), Set[int]] = {}
        self.systems: list[SPGSystem] = []

        self.entity_id_counter = 0

    def create_entity(self, *components) -> int:
        self.entity_id_counter += 1
        self.entities[self.entity_id_counter] = {}

        for component in components:
            component_type = type(component)

            if component_type not in self.components:
                self.components[component_type] = set()
            self.components[component_type].add(self.entity_id_counter)
            self.entities[self.entity_id_counter][component_type] = component

        return self.entity_id_counter

    def get_component(self, component_type: Type[T]) -> Iterable[T]:
        for entity in self.components.get(component_type, []):
            yield self.entities[entity][component_type]
    def get_components(self, *component_types: Type[T]) -> Iterable[tuple[int, list[T]]]:
        try:
            for entity in set.intersection(*[self.components[ct] for ct in component_types]):
                yield entity, [self.entities[entity][ct] for ct in component_types]
        except:
            pass

    def add_component(self, entity_id: int, component: T) -> None:
        component_type = type(component)

        if component_type not in self.components:
            self.components[type(component)] = set()
        
        self.components[component_type].add(entity_id)
        self.entities[entity_id][component_type] = component
    def add_system(self, system: SPGSystem):
        self.systems.append(system)

        # possible change / relocation
        system.on_load()
    def get_entity(self, entity_id: int):
        return entity_id, self.entities[entity_id]
    def get_entity_component(self, entity_id: int, component_type: Type[T]) -> T:
        return self.entities[entity_id][component_type]
    def remove_entity(self, entity_id: int):
        for component_type in self.entities[entity_id].keys():
            self.components[component_type].remove(entity_id)
    def remove_entities(self, *entity_ids):
        for entity_id in entity_ids:
            self.remove_entity(entity_id)
    def run(self, dt) -> None:
        for system in self.systems:
            system.run(dt)
    def remove_system(self, system: SPGSystem):
        system.on_unload()
        self.systems.remove(system)